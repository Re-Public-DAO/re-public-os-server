from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from republic_os.oauth.api.serializers import OAuthSerializer
from republic_os.oauth.models import OAuthState


class OAuthStateViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = OAuthSerializer
    queryset = OAuthState.objects.all()

    def get_queryset(self,):
        queryset = super().get_queryset()

        print(self.request)

        # queryset = queryset.filter(access_token__isnull=False)

        republic_id = self.request.query_params.get('republic_id', None)

        if republic_id is not None:
            queryset = queryset.filter(republic_id=republic_id)

        return queryset
