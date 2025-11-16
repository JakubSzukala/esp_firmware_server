from django.contrib import admin

from .models import EspDevice, HeartbeatSignal

admin.site.register(EspDevice)
admin.site.register(HeartbeatSignal)
