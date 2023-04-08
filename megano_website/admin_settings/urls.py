from django.urls import path

from .views import SettingsAPIView

urlpatterns = [
    path('settings/', SettingsAPIView.as_view(), name='settings'),
]
