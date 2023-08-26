import os
import requests
from django.contrib.auth import get_user_model

url = os.environ.get('RE_PUBLIC_SERVER_URL')


def get_headers():
    headers = {
        "X-Parse-Application-Id": os.environ.get('RE_PUBLIC_APP_ID'),
        "X-Parse-REST-API-Key": os.environ.get('RE_PUBLIC_REST_API_KEY'),
        "Content-Type": "application/json",
    }
    return headers


def login(user):

    headers = get_headers()

    headers['X-Parse-Revocable-Session'] = '1'

    data = {
        "username": os.environ.get('RE_PUBLIC_API_USERNAME'),
        "password": os.environ.get('RE_PUBLIC_API_KEY'),
    }

    # Login to Re-Public server (Parse)
    login_response = requests.post(f'{url}/parse/login', json=data, headers=headers)

    print('login response')
    print(login_response.json())

    parse_user = login_response.json()

    user.re_public_session_token = parse_user['sessionToken']
    user.save()

    return parse_user


def get_parse_user():
    user = get_user_model().objects.first()

    if not user:
        return None

    if not user.re_public_session_token:
        return login(user)

    headers = get_headers()

    headers['X-Parse-Session-Token'] = user.re_public_session_token

    try:

        parse_user_response = requests.get(f'{url}/parse/users/me', headers=headers)

        print(parse_user_response)

        if parse_user_response.status_code != 200:
            raise Exception('Invalid Re-Public session token')

        return parse_user_response.json()

    except Exception as e:
        print(e)
        user.re_public_session_token = None
        user.save()


def query_parse(parse_class, params):

    user = get_user_model().objects.first()

    if not user:
        return None

    if not user.re_public_session_token:

        login(user)

    # If we get here we should have a valid session token with Parse
    headers = get_headers()

    headers['X-Parse-Session-Token'] = user.re_public_session_token

    parse_response = requests.get(f'{url}/parse/classes/{parse_class}', params=params, headers=headers)

    return parse_response.json()['results']
