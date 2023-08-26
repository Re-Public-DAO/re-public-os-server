from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import Device

from .serializers import DeviceSerializer


class DeviceViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
    lookup_field = "name"

    def get_queryset(self, *args, **kwargs):
        # assert isinstance(self.request.user.id, int)
        return self.queryset.all()

    @action(detail=False)
    def me(self, request):
        serializer = DeviceSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
