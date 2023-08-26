from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework import status

from republic_os.connectors.models import OAuthState, Connector
import secrets
import os
import requests

from datetime import datetime

import json
import hashlib

from republic_os.cookie_token_auth import CookieTokenAuthentication


class RePublicServerAccess(BasePermission):

    def has_permission(self, request, view):
        auth_header = request.headers.get('X-Re-Public-Auth')
        if auth_header is None:
            return False

        token_type, token_value = auth_header.split(' ')

        if token_type != 'Token':
            return False

        return True


def file_and_data_are_equal(file_path, data):
    file_hash_algorithm = hashlib.sha256()
    data_hash_algorithm = hashlib.sha256()

    data_hash_algorithm.update(data)

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            file_hash_algorithm.update(data)

    file_hash = file_hash_algorithm.hexdigest()
    data_hash = data_hash_algorithm.hexdigest()

    print(f'file_hash: {file_hash}')
    print(f'data_hash: {data_hash}')

    return file_hash == data_hash


def get_data_from_spotify(spotify_oauth, endpoint):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + spotify_oauth.access_token,
    }

    res = requests.get(f'https://api.spotify.com/v1{endpoint}', headers=headers)

    try:

        res_json = res.json()

        # TODO: Handle pagination/offsets

    except Exception as e:
        print(res)
        print(e)
        res_json = {}

    if res.status_code == 401 and res_json['error'] and res_json['error']['message'] == 'The access token expired':

        body = {
            'refreshToken': spotify_oauth.refresh_token,
        }

        print(body)

        refresh_headers = {
            'Content-Type': 'application/json',
        }

        refresh_res = requests.post(f'{os.environ["RE_PUBLIC_NEXTJS_URL"]}/api/spotify/oauth/refresh/', json=body, headers=refresh_headers)

        print(refresh_res)

        refresh_json = refresh_res.json()

        print(refresh_json)

        spotify_oauth.access_token = refresh_json['access_token']

        spotify_oauth.save()

        headers['Authorization'] = 'Bearer ' + refresh_json['access_token']

        res2 = requests.get('https://api.spotify.com/v1/me', headers=headers)

        res_json = res2.json()

    return res_json


@api_view(['GET'])
def test_ingest(request):
    directory = '/re_public_os_raw_data'

    # Get the latest file by timestamp
    existing_files = os.listdir(directory)

    directories = [entry for entry in existing_files if os.path.isdir(os.path.join(directory, entry))]

    print(directories)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def test(request):

    # client = docker.from_env()
    #
    # containers = client.containers.list()
    #
    # perkeep = [container for container in containers if 'perkeep' in container.name][0]

    spotify_oauth = OAuthState.objects.filter(access_token__isnull=False,).first()

    data = get_data_from_spotify(spotify_oauth, '/me')

    print(data)

    directory = '/re_public_os_raw_data'

    # Get the latest file by timestamp
    existing_files = os.listdir(directory)

    # Filter files based on the presence of filename_part
    profile_files = [file for file in existing_files if 'spotify_profile' in file]

    # Sort the files by last modified time (most recent first)
    sorted_profile_files = sorted(profile_files, key=lambda file: os.path.getmtime(os.path.join(directory, file)),
                          reverse=True)

    most_recent_profile_file = sorted_profile_files[0]

    # Check if the new data downloaded is different from the latest file
    are_equal = file_and_data_are_equal(f'/{directory}/{most_recent_profile_file}', json.dumps(data).encode('utf-8'))

    print(f'are_equal: {are_equal}')

    # If it is different, save the new file
    if not are_equal:

        # Dump raw data into a timestamped file
        with open(f'/re_public_os_raw_data/spotify_profile_{datetime.now().isoformat()}.json', 'w') as f:
            f.write(json.dumps(data))

    endpoints = [
        '/me/top/artists',
        '/me/top/tracks',
        '/me/tracks',
        '/me/shows',
        '/me/playlists',
        '/me/albums',
    ]

    for endpoint in endpoints:
        print(f'Getting {endpoint}')
        endpoint_data = get_data_from_spotify(spotify_oauth, endpoint)

        endpoint_file_name = endpoint.replace('/', '_')

        endpoint_files = [file for file in existing_files if endpoint_file_name in file]

        most_recent_file = None

        if len(endpoint_files) > 0:
            most_recent_file = endpoint_files[0]

        if most_recent_file is None:
            with open(f'/re_public_os_raw_data/spotify_{endpoint_file_name}_{datetime.now().isoformat()}.json',
                      'w') as f:
                f.write(json.dumps(endpoint_data))

        if most_recent_file is not None:
            has_not_changed = file_and_data_are_equal(f'/{directory}/{most_recent_file}', json.dumps(endpoint_data).encode('utf-8'))

            if not has_not_changed:

                with open(f'/re_public_os_raw_data/spotify_{endpoint_file_name}_{datetime.now().isoformat()}.json', 'w') as f:
                    f.write(json.dumps(endpoint_data))

    return Response({
        'message': 'ok',
    })


@api_view(['POST'])
def connect_service(request, connector_id):

    # Look for an existing connection to the service
    oauth_state = OAuthState.objects.filter(connector_id=connector_id).first()

    # If it exists and has a valid token, return 200
    if oauth_state is not None:
        if oauth_state.status == 'Connected':
            return Response({
                'message': 'ok',
            })

        # Here we have a previous attempt to connect a service that failed or is still in progress
        # If there is no access token, but there is a url, we can redirect the user to the url
        if oauth_state.access_token is None and oauth_state.url is not None:
            return Response({
                'message': 'ok',
                'state': oauth_state.state,
                'url': oauth_state.url,
            })

    # If it doesn't exist, create a new one
    if oauth_state is None:

        oauth_state = OAuthState.objects.create(
            connector_id=connector_id,
        )

    re_public_store_token = secrets.token_urlsafe(32)

    oauth_state.status = 'Contacting Re-Public server'
    oauth_state.re_public_store_token = re_public_store_token
    oauth_state.save()

    print('Should have saved OAuthState')

    headers = {
        "X-Parse-Application-Id": os.environ.get('RE_PUBLIC_APP_ID'),
        "X-Parse-REST-API-Key": os.environ.get('RE_PUBLIC_REST_API_KEY'),
        "Content-Type": "application/json",
    }

    url = os.environ.get('RE_PUBLIC_SERVER_URL')

    parse_user = None

    # Check if user has a valid Re-Public session token
    if request.user.re_public_session_token is not None:

        headers['X-Parse-Session-Token'] = request.user.re_public_session_token

        try:

            parse_user_response = requests.get(f'{url}/parse/users/me', headers=headers)

            print(parse_user_response)

            if parse_user_response.status_code != 200:

                raise Exception('Invalid Re-Public session token')

            parse_user = parse_user_response.json()

        except Exception as e:
            print(e)
            request.user.re_public_session_token = None
            request.user.save()

    # Login if necessary
    if parse_user is None or not parse_user['objectId']:

        headers['X-Parse-Revocable-Session'] = '1'

        data = {
            "username": os.environ.get('RE_PUBLIC_API_USERNAME'),
            "password": os.environ.get('RE_PUBLIC_API_KEY'),
        }

        try:

            # Login to Re-Public server (Parse)
            login_response = requests.post(f'{url}/parse/login', json=data, headers=headers)

            print('login response')
            print(login_response.json())

            parse_user = login_response.json()

            request.user.re_public_session_token = parse_user['sessionToken']
            request.user.save()

        except Exception as e:
            oauth_state.set('status', f'Error contacting Re-Public server: {e}')
            return Response({
                'message': 'error',
            })

    # Search for OAuthState object in Re-Public server
    oauth_state_search_params = {
        'where': f'{{"connectorId": "{connector_id}", '
                 f'"user": '
                 f'{{ "__type": "Pointer", '
                 f'"className": "_User", '
                 f'"objectId": "{parse_user["objectId"]}" '
                 f'}}}}'
    }

    oauth_state_search_response = requests.get(f'{url}/classes/OAuthState', params=oauth_state_search_params, headers=headers)

    external_oauth_states = oauth_state_search_response.json()['results']

    external_oauth_state = None

    print(external_oauth_states)

    if len(external_oauth_states) == 1:
        external_oauth_state = external_oauth_states[0]
        if 'url' in external_oauth_state and external_oauth_state['url'] is not None:
            print('url:')
            print(external_oauth_state['url'])
            print('state:')
            print(external_oauth_state['state'])

            # Should return a redirect to the client

            return Response({
                'state': external_oauth_state['state'],
                'url': external_oauth_state['url'],
            })

    if len(external_oauth_states) == 0:

        # Get the CloudInstall object from Re-Public server
        cloud_install_params = {
            'where': f'{{"user": {{ '
                     f'"__type": "Pointer", '
                     f'"className": "_User", '
                     f'"objectId": "{parse_user["objectId"]}" '
                     f'}}}}'
        }

        cloud_install_response = requests.get(f'{url}/classes/CloudInstall', params=cloud_install_params, headers=headers)

        cloud_install = cloud_install_response.json()['results'][0]

        # Get the Connector object from Re-Public server
        connector_params = {
            'where': f'{{"connectorId": "{connector_id}"}}'
        }

        connector_response = requests.get(f'{url}/classes/Connector', params=connector_params, headers=headers)

        connector = connector_response.json()['results'][0]

        # Create a new OAuthState object in Re-Public server
        data = {
            'connectorId': connector_id,
            'instanceAccessKey': re_public_store_token,
            'user': {
                '__type': 'Pointer',
                'className': '_User',
                'objectId': parse_user['objectId'],
            },
            'connector': {
                '__type': 'Pointer',
                'className': 'Connector',
                'objectId': connector['objectId'],
            },
            'instanceDomain': cloud_install['domain'],
            'cloudInstall': {
                '__type': 'Pointer',
                'className': 'CloudInstall',
                'objectId': cloud_install['objectId'],
            },
        }

        create_server_record_response = requests.post(f'{url}/classes/OAuthState', json=data, headers=headers)

        print('Create server record response: ')
        print(create_server_record_response.json())

        external_oauth_state = create_server_record_response.json()

    if external_oauth_state is not None and 'url' not in external_oauth_state:

        auth_url_data = {
            'connectorId': connector_id,
        }

        # Get the OAuthUrl and redirect the user to it
        oauth_url_response = requests.post(f'{url}/parse/functions/getConnectorAuthUrl', json=auth_url_data,
                                           headers=headers)

        oauth_url_json = oauth_url_response.json()

        print(oauth_url_json)

        if 'result' not in oauth_url_json:
            oauth_state.set('status', f'Error contacting Re-Public server: {oauth_url_json}')
            return Response({
                'message': 'error',
            })

        oauth_data = oauth_url_response.json()['result']

        if 'url' not in oauth_data:
            oauth_state.set('status', f'Error contacting Re-Public server: {oauth_data}')
            return Response({
                'message': 'error',
            })

        print(oauth_data)

        oauth_state.scope = oauth_data['scope']
        oauth_state.state = oauth_data['state']
        oauth_state.url = oauth_data['url']

        oauth_state.save()

        return Response({
            'state': oauth_data['state'],
            'url': oauth_data['url'],
        })

    return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny,])
def receive_oauth_data(request, connector_id):

    print('receive_oauth_data')

    print(f'connector_id: {connector_id}')

    auth_header = request.headers.get('X-Re-Public-Auth')

    token_type, token_value = auth_header.split(' ')

    oauth_state = OAuthState.objects.filter(
        connector_id=connector_id,
        # re_public_store_token=token_value,
    ).first()

    print(f'token_type: {token_type}')
    print(f'token_value: {token_value}')

    if oauth_state is None:
        return Response({
            'message': 'Unauthorized',
        }, status=status.HTTP_401_UNAUTHORIZED)

    print('request.data')
    print(request.data)

    for key, value in request.data.items():
        print(f'{key}: {value}')
        if type(value) == str:
            print(len(value))
        setattr(oauth_state, key, value)

    oauth_state.save()

    return Response({
        'message': 'ok',
    })


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication,])
def get_connectors(request):

    return Response({
        'message': 'ok',
        'connectors': Connector.objects.all(),
    })