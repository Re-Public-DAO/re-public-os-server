from django.contrib.auth import get_user_model
from django.db import models
from republic_os.utils.models import RePublicModel


class Device(RePublicModel):

    name_on_device = models.CharField(max_length=255)
    name_in_os = models.CharField(max_length=255, null=True)
    uuid = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    system_name = models.CharField(max_length=255, null=True)
    system_version = models.CharField(max_length=255, null=True)
    total_disk_capacity = models.CharField(max_length=255, null=True)
    total_memory = models.CharField(max_length=255, null=True)
    is_tablet = models.BooleanField(default=False)
    is_mobile = models.BooleanField(default=False)
    is_desktop = models.BooleanField(default=False)
    qr_code_key = models.CharField(max_length=255, null=True, blank=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='devices', null=True)

    def __str__(self):
        return self.name_on_device or self.name_in_os or self.uuid or self.qr_code_key


class DeviceConnection(RePublicModel):

    network_id = models.CharField(max_length=255, null=True)
    node_id = models.CharField(max_length=255, null=True)
    ip_address = models.CharField(max_length=255, null=True)

    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='connection', null=True)

    def __str__(self):
        return self.device.name_on_device or self.device.name_in_os or self.device.uuid or self.device.qr_code_key