import os
from shutil import disk_usage

from rest_framework import permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.conf import settings


def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size


@api_view(['GET'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def get_storage_info(request, republic_id):

    total, used, free = disk_usage("/")
    media_size = get_directory_size('/re_public_os_raw_data')
    app_size = get_directory_size('/app')

    data = {
        'usedDiskSpace': used,
        'freeDiskSpace': free,
        'mediaSpaceUsed': media_size,
        'republicAppSpaceUsed': app_size
    }

    return Response(data)


def list_dir_contents(path):
    contents = []
    try:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            full_path = os.path.normpath(full_path)
            client_path = full_path.replace('/re_public_os_raw_data', '')
            if os.path.isdir(full_path):
                contents.append({
                    'name': entry,
                    'type': 'folder',
                    'path': client_path,
                    'children': list_dir_contents(full_path)
                })
            else:
                contents.append({
                    'name': entry,
                    'type': 'file',
                    'path': client_path,
                })
    except OSError:
        pass  # Optionally handle errors, e.g., permission issues
    return contents


@api_view(['GET'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def get_file_browser_contents(request, republic_id):

    full_path = os.path.join(settings.BASE_DIR, '..', 're_public_os_raw_data')

    contents = list_dir_contents(full_path)

    return Response(contents)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def get_file_contents(request, republic_id):
    # Get the 'path' query parameter
    file_path = request.data.get('path', None)

    if not file_path:
        return Response({"error": "No path provided"}, status=status.HTTP_400_BAD_REQUEST)

    if file_path.startswith('/'):
        file_path = file_path[1:]

    local_path = os.path.join(settings.BASE_DIR, '..', 're_public_os_raw_data', file_path)

    # Optional: Add security checks here to prevent unauthorized access

    try:
        # Read the file content
        with open(local_path, 'r') as file:
            content = file.read()

        return Response({"content": content})

    except FileNotFoundError:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
    except IOError:
        return Response({"error": "Error reading file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
