from django.urls import path

from republic_os.connectors.views import (
    connect_service,
    receive_oauth_data,
    get_connectors,
    test,
    test_ingest,
)

app_name = "connectors"
urlpatterns = [
    path("", view=get_connectors, name="get_connectors"),
    path("test/", view=test, name="test"),
    path("test-ingest/", view=test_ingest, name="test_ingest"),
    path("<str:connector_id>/", view=connect_service, name="connect_service"),
    path("<str:connector_id>/oauth/", view=receive_oauth_data, name="receive_oauth_data"),
]