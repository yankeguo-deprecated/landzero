from django.urls import path

from . import views

urlpatterns = [
    path('callback_mp', views.callback_mp, name='callback_mp')
]
