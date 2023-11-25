from rest_framework import serializers

from republic_os.oauth.models import OAuthState


class OauthStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuthState
        fields = '__all__'