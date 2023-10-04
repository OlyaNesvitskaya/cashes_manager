from django.urls import path
from .views import *

app_name = 'manager'

urlpatterns = [
    path('', index, name='home'),
    path('change_process_state/<str:profile_serial>/', change_process_state, name='change_process_state'),
    path('edit_profile/<str:profile_serial>/', edit_profile, name='edit')
]


