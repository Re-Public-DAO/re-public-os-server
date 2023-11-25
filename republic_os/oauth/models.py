from django.db import models

from republic_os.connectors.constants import CONNECTOR_ID_SPOTIFY
from republic_os.utils.models import RePublicModel


class OAuthState(RePublicModel):

    state = models.CharField(max_length=255)
    scope = models.CharField(max_length=500, null=True)
    code = models.CharField(max_length=600, null=True)
    access_token = models.CharField(max_length=255, null=True)
    refresh_token = models.CharField(max_length=255, null=True)
    expires_at = models.DateTimeField(null=True)
    wallet_address = models.CharField(max_length=255, null=True)
    re_public_user_id = models.CharField(max_length=255, null=True)
    code_verifier = models.CharField(max_length=255, null=True)
    re_public_store_token = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=500, null=True)
    sync_interval_minutes = models.IntegerField(null=True, blank=True)

    connector = models.ForeignKey('connectors.Connector', to_field='republic_id', on_delete=models.CASCADE, null=True, related_name='oauths')

    def __str__(self):
        return self.connector_id

    # def sync_data(self):
    #     if self.connector_id == CONNECTOR_ID_SPOTIFY:
    #         spotify_sync(self)
