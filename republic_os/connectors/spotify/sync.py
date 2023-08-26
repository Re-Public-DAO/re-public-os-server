import hashlib
import os
from datetime import datetime
import json
import requests


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


def sync(spotify_oauth):
    print('called sync()')

    if not hasattr(spotify_oauth, 'access_token'):
        print('No access token')
        return

    data = get_data_from_spotify(spotify_oauth, '/me')

    print(data)

    directory = '/re_public_os_raw_data/spotify'

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the latest file by timestamp
    existing_files = os.listdir(directory)

    if len(existing_files) > 0:

        existing_files = sorted(existing_files, key=lambda file: os.path.getmtime(os.path.join(directory, file)),
                                      reverse=True)

    endpoints = [
        '/me'
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
            with open(f'/{directory}/spotify_{endpoint_file_name}_{datetime.now().isoformat()}.json',
                      'w') as f:
                f.write(json.dumps(endpoint_data))

        if most_recent_file is not None:
            has_not_changed = file_and_data_are_equal(f'/{directory}/{most_recent_file}',
                                                      json.dumps(endpoint_data).encode('utf-8'))

            if not has_not_changed:
                with open(f'/{directory}/spotify_{endpoint_file_name}_{datetime.now().isoformat()}.json',
                          'w') as f:
                    f.write(json.dumps(endpoint_data))
