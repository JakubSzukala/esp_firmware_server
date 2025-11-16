from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:chip_id>/", views.device, name="device"),
]
