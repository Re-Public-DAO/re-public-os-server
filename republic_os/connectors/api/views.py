from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from ..models import Connector, ConnectorSync


class ConnectorViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = Connector
    queryset = Connector.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        return queryset


class ConnectorSyncViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = ConnectorSync
    queryset = ConnectorSync.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        return queryset


