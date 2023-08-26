from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from ..models import Event

from .serializers import EventSerializer


class OAuthStateViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        return queryset


