from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from ..models import OAuthState, Connector

from .serializers import OAuthSerializer, ConnectorSerializer


class ConnectorViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = Connector
    queryset = OAuthState.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        return queryset


class OAuthStateViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = OAuthSerializer
    queryset = OAuthState.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        # queryset = queryset.filter(access_token__isnull=False)

        connector_id = self.request.query_params.get('connector_id', None)

        if connector_id is not None:
            queryset = queryset.filter(connector_id=connector_id)

        return queryset


