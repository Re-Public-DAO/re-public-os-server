from rest_framework import serializers

from republic_os.oauth.models import OAuthState


class OAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuthState
        fields = '__all__'

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }