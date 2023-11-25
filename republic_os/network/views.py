import os
import requests
from rest_framework.authentication import TokenAuthentication

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from republic_os.cookie_token_auth import CookieTokenAuthentication
from republic_os.devices.models import DeviceConnection, Device


def get_network_id():
    networks_conf_path = '/var/lib/zerotier-one/controller.d/network'
    conf_files = os.listdir(networks_conf_path)

    network_id = None

    for file in conf_files:
        if not file.endswith('local.conf'):
            network_id = os.path.splitext(file)[0]
            print(network_id)

        if network_id:
            break

    return network_id


def zerotier_request(endpoint, method='GET', json=None):
    with open('/var/lib/zerotier-one/authtoken.secret', 'r') as f:
        api_key = f.read().strip()

    network_id = get_network_id()

    if not network_id:
        raise Exception('No ZeroTier network found')

    base_url = f'http://republic-os-local-zerotier:9993/controller/network/{network_id}'

    url = f'{base_url}/{endpoint}'

    print(url)

    headers = {
        'Content-Type': 'application/json',
        'X-ZT1-AUTH': api_key
    }

    if method == 'DELETE':
        return requests.delete(url, headers=headers).json()

    if method == 'POST':
        return requests.post(url, headers=headers, json=json).json()

    return requests.get(url, headers=headers).json()


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication, TokenAuthentication])
def test(request):
    # Is the ZeroTier network online?
    member_info = zerotier_request(f'member/41e664ecd6')

    print(member_info)

    return Response({
        'message': 'ok',
    })


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
def status(request):
    # Is the ZeroTier network online?

    return Response({
        'message': 'ok',
    })


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication, TokenAuthentication])
def network_info(request, node_id):

    network_info = zerotier_request(f'')

    return Response({
        'message': 'ok',
        'network_info': network_info,
    })


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication, TokenAuthentication])
def node_info(request, node_id):

    node_info = zerotier_request(f'member/{node_id}')

    print(node_info)

    connection = DeviceConnection.objects.filter(
        node_id=node_id,
    ).first()

    if connection and 'ipAssignments' in node_info and len(node_info['ipAssignments']) > 0:
        connection.ip_address = node_info['ipAssignments'][0]
        connection.save()

    return Response({
        'message': 'ok',
        'node_info': node_info,
    })


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication, TokenAuthentication])
def nodes(request):
    # If the network is online, get all nodes
    authorized = request.GET.get('authorized', True)

    if authorized == 'false':
        authorized = False
    if authorized == 'true':
        authorized = True

    nodes_raw = zerotier_request('member')

    node_ids = nodes_raw.keys()

    nodes = []

    network_id = get_network_id()

    for node_id in node_ids:
        print(node_id)
        if node_id not in network_id:
            member_info = zerotier_request(f'member/{node_id}')
            print(member_info)
            print(f'authorized: {authorized}')
            print(f'member_info[authorized]: {member_info["authorized"]}')
            if authorized != member_info['authorized']:
                continue
            nodes.append(member_info)

    sorted_nodes = sorted(nodes, key=lambda x: x['creationTime'], reverse=True)

    return Response({
        'message': 'ok',
        'nodes': sorted_nodes,
    })


@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication, TokenAuthentication])
def node_connect(request, node_id):

    print('node_connect')

    if 'uuid' not in request.data:
        return Response({
            'message': 'Invalid request',
        })

    # Add device node as member of the ZeroTier network
    add_member_data = {
        'authorized': True,
        'allowManaged': True,
    }

    # print('requesting')

    response = zerotier_request(f'member/{node_id}', method='POST', json=add_member_data)

    # print(response)
    #
    # print('allow managed response')
    #
    # allow_managed_response = zerotier_request(f'', method='POST', json={'allowManaged': True})
    #
    # print(allow_managed_response)

    zerotier_network_id = get_network_id()

    device = Device.objects.filter(uuid=request.data['uuid']).first()

    if 'ipAssignments' in response and len(response['ipAssignments']) > 0:
        ip_address = response['ipAssignments'][0]

        # Save the ZeroTier data to the DeviceConnection
        connection, created = DeviceConnection.objects.get_or_create(
            device=device,
        )

        connection.network_id = zerotier_network_id
        connection.node_id = node_id
        connection.ip_address = ip_address
        connection.save()

        return Response({
            'message': 'ok',
        })

    # Save the ZeroTier data to the DeviceConnection
    connection, created = DeviceConnection.objects.get_or_create(
        device=device,
    )

    connection.network_id = zerotier_network_id
    connection.node_id = node_id
    connection.save()

    # TODO: The ZeroTier container may need to be restarted here in order to assign an IP address. Not sure why.

    return Response({
        'message': 'ok',
    })


@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
def node_disconnect(request, node_id):

    zerotier_request(f'member/{node_id}', method='DELETE')

    return Response({
        'message': 'ok',
    })


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication,])
def connections(request):

    connections = DeviceConnection.objects.all()

    return Response({
        'message': 'ok',
        'connections': connections,
    })
