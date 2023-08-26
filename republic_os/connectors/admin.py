from django.contrib import admin
from republic_os.connectors.models import OAuthState, Connector

admin.site.register(OAuthState)
admin.site.register(Connector)
