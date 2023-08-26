import json

import requests
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import qrcode
import base64
import secrets
from io import BytesIO
import os
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist

from republic_os.cookie_token_auth import CookieTokenAuthentication
from republic_os.devices.models import Device, DeviceConnection


@api_view(['POST'])
def connect_vpn(request):
    return Response({
        'message': 'ok',
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def add_device(request):
    if not request.data['qr_code_key'] \
            or not request.data['uuid']:
        return Response({
            'message': 'Invalid request',
        }, status=400)

    device = Device.objects.filter(qr_code_key=request.data['qr_code_key']).first()

    if not device:
        return Response({
            'message': 'Device not found',
        }, status=404)

    try:
        connection = device.connection

    except ObjectDoesNotExist:
        print('No connection found')
        connection = None

    try:
        user = device.user

    except ObjectDoesNotExist:
        print('No user found for device')
        user = None

    if not user:
        return Response({
            'message': 'User not found for device',
        }, status=500)

    if connection:

        # TODO: Verify and replace connection if necessary

        return Response({
            'message': 'Device already connected',
        }, status=200)

    device.uuid = request.data['uuid']
    device.name_on_device = request.data['name']
    device.manufacturer = request.data['manufacturer']
    device.brand = request.data['brand']
    device.system_name = request.data['system_name']
    device.system_version = request.data['system_version']
    device.total_disk_capacity = request.data['total_disk_capacity']
    device.total_memory = request.data['total_memory']
    device.is_tablet = request.data['is_tablet']
    device.is_mobile = request.data['is_mobile']
    device.is_desktop = request.data['is_desktop']
    device.save()

    # Get the ZeroTier Network Id for the device to connect to
    headers = {
        'Content-Type': 'application/json',
        'X-ZT1-AUTH': os.environ['ZEROTIER_API_TOKEN']
    }

    base_url = 'http://republic_os_local_zerotier:9993/controller/network'

    response = requests.get(base_url, headers=headers, params={})

    if response.status_code != 200:
        return Response({
            'message': 'ZeroTier API error',
        }, status=500)

    list_of_network_ids = response.json()

    print(list_of_network_ids)

    if len(list_of_network_ids) == 0:
        return Response({
            'message': 'No ZeroTier networks found',
        }, status=500)

    zerotier_network_id = list_of_network_ids[0]

    token, _ = Token.objects.get_or_create(user=device.user)

    response = Response({
        'message': 'ok',
        'zerotier_network_id': zerotier_network_id,
        'token': token.key,
    })

    response.set_cookie('auth_token', token.key, httponly=True, samesite='None', secure=True)

    return response


@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
def check_for_device(request):

    print(request.data)
    print(request.data['qr_code_key'])

    if not request.data['qr_code_key']:
        return Response({
            'message': 'Invalid request',
        }, status=400)

    device = Device.objects.filter(
        qr_code_key=request.data['qr_code_key'],
        uuid__isnull=False,
    ).exclude(uuid='').first()

    print(device)

    if not device:
        return Response({
            'message': 'Device not found',
        }, status=404)

    return Response({
        'message': 'Has device',
    })


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
def generate_qr_code(request):
    # Check to see if any devices are waiting to be connected
    existing_devices = Device.objects.filter(qr_code_key__isnull=False)

    # If there is, use it to generate the QR code
    # We only want one device to be waiting at a time
    if existing_devices.count() == 1:
        qr_code_key = existing_devices[0].qr_code_key
    else:
        # Generate QR code key
        qr_code_key = secrets.token_hex(16)
        # Save the QR code key to a new device
        new_device = Device.objects.create(qr_code_key=qr_code_key)
        new_device.user = request.user
        new_device.save()

    # Add it to the URL as a parameter
    qr_code_data = {
        'qr_code_key': qr_code_key,
        'api_url': f'{os.environ["RE_PUBLIC_DJANGO_URL"]}'
    }

    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(json.dumps(qr_code_data))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        data_url = f"data:image/png;base64,{img_str}"
        return Response({
            'dataUrl': data_url,
            'qrCodeKey': qr_code_key,
        })
    except Exception as e:
        print('Error generating QR code:', e)
        return Response({'error': 'Error generating QR code'}, status=500)


@api_view(['POST'])
def link_device(request):
    # Get the QR code key from the request
    # Find the device with that key

    return Response({
        'message': 'ok',
    })
