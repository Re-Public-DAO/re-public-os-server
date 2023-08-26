from rest_framework import serializers
from ..models import AppInstall


class AppInstallSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInstall
        fields = [
            "app_store_id",
        ]

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }
