from rest_framework import serializers
from ..models import OAuthState, Connector


class ConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connector
        fields = '__all__'


class OAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuthState
        fields = '__all__'

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }
