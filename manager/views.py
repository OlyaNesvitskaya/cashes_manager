from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import NON_FIELD_ERRORS
from .managers import *
from .forms import *


def index(request):
    search_string = request.GET.get('search_string', '').strip().lower()
    field_to_sorted = request.GET.get('sorted_by_field')
    profiles = get_profiles_state(search_string, field_to_sorted)
    return render(request, 'manager/index.html', {'profiles': profiles, 'heading': 'Перечень касс',
                                                  'search_string': search_string})


def change_process_state(request, profile_serial):
    profile = get_profile(profile_serial)
    if request.POST.get("stop_process"):
        process = get_process(profile.id)
        if profile.enabled and not psutil.pid_exists(process.pid):
            delete_process(process.id_profile)
            message = (f'Ошибка в остановке кассы с серийным номером №{profile.serial}, '
                       f'так как процесс в системе отсутствовал')
        else:
            stop_cashbox(profile)
            message = f'Касса с серийным номером №{profile.serial} остановлена.'
        profile.enabled = False
        profile.save()
    else:
        profile.enabled = True
        launch_cashbox(profile)
        profile.save()
        message = f'Касса с серийным номером №{profile.serial} запущена.'
    messages.success(request, message)
    search_string = request.POST.get('search_string', '')
    return HttpResponseRedirect(reverse_querystring('manager:home', query_kwargs={'search_string': search_string}))


def edit_profile(request, profile_serial):
    profile = get_profile(profile_serial)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile_pid = getattr(profile, 'process', False)
            if profile.enabled and not profile_pid:
                launch_cashbox(profile)
            elif not profile.enabled and profile_pid:
                stop_cashbox(profile)
            form.save()
            messages.success(request, 'Профиль был обновлен успешно.')
            return HttpResponseRedirect(reverse('manager:home'))
        else:
            form_errors = form.errors[NON_FIELD_ERRORS]
            return render(request, 'manager/edit_profile.html', {'form': form,
                                                'heading': 'Изменение профиля', 'errors': form_errors})
    form = ProfileForm(instance=profile)
    return render(request, 'manager/edit_profile.html', {'form': form, 'heading': 'Изменение профиля'})


def error_404(request, exception):
    return render(request, 'manager/error_404.html', status=404)


def error_500(request):
    return render(request, 'manager/error_500.html', status=500)