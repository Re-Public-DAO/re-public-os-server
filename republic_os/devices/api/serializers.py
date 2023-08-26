from rest_framework import serializers
from ..models import Device, DeviceConnection


class DeviceConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceConnection
        fields = [
            "device",
            "network_id",
            "node_id",
            "ip_address",
        ]


class DeviceSerializer(serializers.ModelSerializer):
    connection = DeviceConnectionSerializer(read_only=True)

    class Meta:
        model = Device
        fields = [
            "name_in_os",
            "name_on_device",
            "uuid",
            "manufacturer",
            "model",
            "connection",
        ]

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }
