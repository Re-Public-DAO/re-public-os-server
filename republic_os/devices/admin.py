from django.contrib import admin
from republic_os.devices.models import Device, DeviceConnection

admin.site.register(Device)
admin.site.register(DeviceConnection)
