from django.urls import path

from republic_os.network.views import (
    status,
    nodes,
    node_info,
    network_info,
    node_disconnect,
    node_connect,
    test,
)

app_name = "network"
urlpatterns = [
    path("test/", view=test, name="test"),
    path("status/", view=status, name="status"),
    path("info/", view=network_info, name="network_info"),
    path("nodes/", view=nodes, name="nodes"),
    path("nodes/<str:node_id>/connect/", view=node_connect, name="node_connect"),
    path("nodes/<str:node_id>/disconnect/", view=node_disconnect, name="node_disconnect"),
    path("nodes/<str:node_id>/", view=node_info, name="node_info"),
]