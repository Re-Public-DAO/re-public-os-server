from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import AppInstall

from .serializers import AppInstallSerializer


class AppInstallViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = AppInstallSerializer
    queryset = AppInstall.objects.all()
    lookup_field = "app_store_id"

    def get_queryset(self, *args, **kwargs):
        # assert isinstance(self.request.user.id, int)
        return self.queryset.all()

    @action(detail=False)
    def me(self, request):
        serializer = AppInstallSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
