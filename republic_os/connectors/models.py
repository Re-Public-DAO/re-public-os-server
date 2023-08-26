from django.db import models

from republic_os.connectors.constants import CONNECTOR_ID_SPOTIFY
from republic_os.utils.models import RePublicModel
from .spotify.sync import sync as spotify_sync


# Tracks the install and status of a connector
class Connector(RePublicModel):
    name = models.CharField(max_length=255)
    republic_id = models.CharField(max_length=255, unique=True)
    is_installed = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    version_number = models.CharField(max_length=10, null=True)
    build_number = models.CharField(max_length=20, null=True)


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
    connector_id = models.CharField(max_length=255)
    re_public_store_token = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.connector_id

    def sync_data(self):
        if self.connector_id == CONNECTOR_ID_SPOTIFY:
            spotify_sync(self)


class ConnectorSync(RePublicModel):

    status = models.CharField(max_length=255, null=True)
    error = models.CharField(max_length=255, null=True)
    completed_at = models.DateTimeField(null=True)

    oauth_state = models.ForeignKey(OAuthState, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.status


class RawFileIngest(RePublicModel):

    status = models.CharField(max_length=255, null=True)
    error = models.CharField(max_length=255, null=True)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.status