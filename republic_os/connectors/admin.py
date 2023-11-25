from django.contrib import admin
from republic_os.connectors.models import Connector, ConnectorSync


admin.site.register(Connector)
admin.site.register(ConnectorSync)
