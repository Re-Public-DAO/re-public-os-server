from django.urls import path

from republic_os.connectors.views import (
    receive_oauth_data,
    test,
    test_ingest,
    ConnectorListView,
    ConnectorView,
    get_authenticated_connectors_list,
    start_sync,
    get_commits,
    get_connector_syncs,
)

app_name = "connectors"
urlpatterns = [
    path("", view=ConnectorListView.as_view(), name="get_connectors"),
    path("authenticated/", view=get_authenticated_connectors_list, name="get_authenticated_connectors"),
    path("test/", view=test, name="test"),
    path("test-ingest/", view=test_ingest, name="test_ingest"),
    path("<str:republic_id>/", view=ConnectorView.as_view(), name="get_connector"),
    path("<str:republic_id>/oauth/", view=receive_oauth_data, name="receive_oauth_data"),
    path("<str:republic_id>/sync/", view=start_sync, name="start_sync"),
    path("<str:republic_id>/commits/", view=get_commits, name="get_commits"),
    path("<str:republic_id>/history/", view=get_connector_syncs, name="get_connector_syncs"),
]