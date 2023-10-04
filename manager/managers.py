import os
import json
import psutil
import requests
import subprocess
import platform
from django.utils.http import urlencode
from .services import *


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage: reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


if platform.system() == 'Windows':
    path_to_profiles = 'C:\Program Files (x86)\checkbox.kasa.manager\profiles'
else:
    path_to_profiles = os.path.join(os.getcwd(), 'checkbox.kasa.manager/profiles')


def run_all_cashboxes(profiles: list = None) -> None:
    """Launches unlaunched cashboxes"""
    if profiles is None:
        profiles = get_profiles()
    for profile in profiles:
        if profile.enabled and not (getattr(profile, 'process', False)):
            launch_cashbox(profile)


def update_profiles() -> None:
    """ If there isn't profile in the database, add it;
     if it exists in the database, but not in the catalog, delete it """

    profiles_in_db = set(i.serial for i in get_profiles())
    profiles_in_file = set(os.listdir(path_to_profiles))
    profiles_to_delete_from_db = profiles_in_db - profiles_in_file
    profile_add_to_db = profiles_in_file - profiles_in_db
    [delete_profile(serial) for serial in profiles_to_delete_from_db]

    for dir in profile_add_to_db:
        path_to_profile = os.path.join(path_to_profiles, dir)
        with open(os.path.join(path_to_profile, 'config.json')) as f:
            file = json.loads(f.read())
            port = file["web_server"]['port']
            create_profile(name=dir, serial=dir, path=path_to_profile, port=port)

    processes = get_processes()
    for process in processes:
        if not psutil.pid_exists(process.pid):
            delete_process(process.id_profile)


def get_profiles_state(search_string: str = None, field_to_sorted: str = None) -> list:
    """Return all profiles with shift field."""

    update_profiles()

    if search_string not in ('открыта', 'закрыта', ''):
        all_profiles = filter_profiles(search_string)
    elif field_to_sorted and field_to_sorted != 'shift':
        all_profiles = get_sorted_profiles(field_to_sorted)
    else:
        all_profiles = get_profiles()

    run_all_cashboxes(all_profiles)

    all_profiles = get_shift_state(all_profiles)

    if search_string in ('открыта', 'закрыта'):
        all_profiles = [i for i in all_profiles if i.shift == search_string]

    if field_to_sorted == 'shift':
        all_profiles = sorted(all_profiles, key=lambda profile: profile.shift)

    return all_profiles


def get_shift_state(all_profiles: list) -> list:
    """Make request to api and get shift state adding it to each profile.
     Return all profiles."""

    for profile in all_profiles:
        if getattr(profile, 'process', False):
            profile.shift = 'открыта'
            # request to api
            '''try:
                    response = requests.get(f'http://127.0.0.1:{profile.port}/api/v1/shift')
                    if response.status_code == 200:
                        if response.json() != {"message": "Зміну не відкрито"}:
                            profile.shift = 'открыта'
                        else:
                            profile.shift = 'закрыта'
                    else:
                            profile.shift = 'Закрыта' 
                except:
                    pass'''

        else:
            profile.shift = 'закрыта'
    return all_profiles


def launch_cashbox(profile: Profile) -> None:
    """Run cashbox emulator in a new process, record process data to the process table."""

    new_process = subprocess.Popen(os.path.join(profile.path, 'checkbox_kasa.exe'), cwd=profile.path)
    create_process(profile, pid=new_process.pid)
    profile.save()


def stop_cashbox(profile_id):
    """Stop cashbox emulator and delete process data from the process table."""

    pid = get_process(profile_id).pid

    if platform.system() == 'Windows':
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=pid))
    else:
        psutil.Process(pid).terminate()
    delete_process(profile_id)


