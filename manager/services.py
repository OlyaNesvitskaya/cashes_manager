from .models import *
from django.db.models import Q


def create_profile(name: str, port: int, path: str, serial: str, note=None) -> None:
    """Create new object of Profile"""
    new_profile = Profile(name=name, serial=serial, port=port, path=path, note=note)
    new_profile.save()


def get_profiles() -> list:
    """Return a QuerySet of Profiles objects"""
    return Profile.objects.all()


def get_sorted_profiles(field) -> list:
    """Return a QuerySet of Profiles objects for a given profile's field"""
    return Profile.objects.order_by(field)


def filter_profiles(search_string) -> list:
    """Return a QuerySet of Profiles objects for a given search string"""
    if search_string in ('да', 'нет'):
        enabled_value = (False, True)[search_string == 'да']
        profiles = Profile.objects.filter(enabled=enabled_value)
    else:
        profiles = Profile.objects.filter(Q(name__contains=search_string) | Q(serial__contains=search_string)
                                          | Q(port__contains=search_string))
    return profiles


def get_profile(serial: str) -> Profile:
    """Return requested profile by serial. """
    profile = Profile.objects.get(serial=serial)
    return profile


def update_profile(serial: str, fields_to_change: dict) -> None:
    """Update requested profile by serial. """
    profile = get_profile(serial)
    for field in fields_to_change:
        profile.field = fields_to_change.get(field)
    profile.save()


def delete_profile(serial: str) -> None:
    """Delete requested profile by serial. """
    profile = get_profile(serial=serial)
    profile.delete()


def create_process(profile: Profile, pid: int) -> None:
    """Create new object of Process"""
    new_process = Process(id_profile=profile, pid=pid)
    new_process.save()


def get_processes() -> list:
    """Return a QuerySet of Process objects"""
    process = Process.objects.all()
    return process


def get_process(profile_id: int) -> Process:
    """Return requested process by profile_id. """
    process = Process.objects.get(id_profile_id=profile_id)
    return process


def delete_process(profile_id: int) -> None:
    """Delete requested process by profile_id. """
    process = get_process(profile_id)
    process.delete()
