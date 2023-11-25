from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from republic_os.oauth.models import OAuthState


@api_view(['GET'])
def get_oauth(request, republic_id):
    if republic_id is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    oauth = OAuthState.objects.filter(connector__republic_id=republic_id).first()

    if oauth is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_200_OK)