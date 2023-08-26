from django.contrib.auth import get_user_model, login, authenticate
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from republic_os.cookie_token_auth import CookieTokenAuthentication
from republic_os.utils.parse import get_parse_user, query_parse


@api_view(['GET'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def test(request):

    print(request.META)

    return Response({
        'message': 'ok',
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def login(request):

    if 'username' not in request.data or 'password' not in request.data:
        return Response({
            'message': 'Invalid request',
        })

    username = request.data['username']
    password = request.data['password']

    user = authenticate(request, username=username, password=password)

    if not user:
        raise AuthenticationFailed('Invalid credentials')

    token, _ = Token.objects.get_or_create(user=user)

    response = Response({
        'message': 'ok',
    })

    # Set the token as a cookie in the response
    response.set_cookie('auth_token', token.key, httponly=True, samesite='None', secure=True)

    return response


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
def me(request):

    if not request.user.is_authenticated:
        return Response({
            'message': 'Not logged in',
        }, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'message': 'ok',
        'user': {
            'username': request.user.username,
            'name': request.user.name,
            'email': request.user.email,
        }
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def unlock(request):

    if 'secret' not in request.data or 'username' not in request.data or 'password' not in request.data:
        return Response({
            'message': 'Invalid request',
        })

    user_model = get_user_model()

    username = request.data['username']
    password = request.data['password']

    new_user = user_model.objects.create_superuser(username, '', password)

    parse_user = get_parse_user()

    if not parse_user:
        return Response({
            'message': 'Parse user not found',
        })

    cloud_install_params = {
        'where': f'{{"user": '
                 f'{{ "__type": "Pointer", '
                 f'"className": "_User", '
                 f'"objectId": "{parse_user["objectId"]}" '
                 f'}}}}'
    }

    cloud_install_response = query_parse('CloudInstall', cloud_install_params)

    if len(cloud_install_response) == 0:
        return Response({
            'message': 'No cloud install found',
        })

    cloud_install = cloud_install_response[0]

    unlock_token = cloud_install['unlockToken']

    secret = request.data['secret']

    if unlock_token != secret:
        return Response({
            'message': 'Invalid unlock token',
        })

    token, _ = Token.objects.get_or_create(user=new_user)
    response = Response({"message": f"Superuser {new_user.username} created successfully."}, status=status.HTTP_201_CREATED)
    # Set the token as a cookie in the response
    response.set_cookie('auth_token', token.key, httponly=True, samesite='None', secure=True)

    # Create ZeroTier network
    # Join server to the network as a node
    return response


@api_view(['GET'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def unlocked(request):

    user_model = get_user_model()

    user_count = user_model.objects.count()

    return Response({
        'message': 'ok',
        'unlocked': user_count > 0,
    })
