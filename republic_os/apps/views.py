from rest_framework.decorators import api_view
from rest_framework.response import Response
from republic_os.apps.models import AppInstall
# import docker
# import requests
# import os
# from republic_os.apps.tasks import install_app

# client = docker.from_env()


# @api_view(['POST'])
# def install(request):
#
#     if request.method == 'POST':

        # app_store_id = request.data['app_store_id']
        #
        # try:
        #
        #     existing_install = AppInstall.objects.get(app_store_id=app_store_id)
        #
        #     if existing_install:
        #         return Response({
        #             'status': 500,
        #             'message': 'That app is already installed'
        #         })
        #
        # except AppInstall.DoesNotExist:
        #     pass
        #
        # # Create a new AppInstall to track progress and report status to the UI
        # app_install = AppInstall(app_store_id=app_store_id, status='start')
        # app_install.save()
        #
        #
        #
        # # Get Docker image from main Re-Public server
        # params = {
        #     'where': f'{{"appStoreId": "{app_store_id}"}}'
        # }
        #
        # headers = {
        #     'X-Parse-Application-Id': os.environ['RE_PUBLIC_API_APP_ID'],
        #     'X-Parse-REST-API-Key': os.environ['RE_PUBLIC_REST_API_KEY'],
        #     'X-Parse-Revocable-Session': '1',
        # }
        #
        # response = requests.get(f'{os.environ["RE_PUBLIC_API_URL"]}/classes/App', params=params, headers=headers)
        #
        # app_list = response.json()['results']
        #
        # print(len(app_list))
        #
        # if len(app_list) == 1:
        #     app = app_list[0]
        #
        #     print('calling install_app')
        #
        #     install_app.delay(app,)
        #
        #     return Response(response.json())

        # return Response(response.json())

    # return Response({
    #     'status': 404
    # })


# @api_view(['GET'])
# def app_status(request, app_store_id):
#
#     try:
#         app_install = AppInstall.objects.get(app_store_id=app_store_id)
#
#         if not app_install:
#             return Response({
#                 'status': 'App not installed',
#             })
#     except AppInstall.DoesNotExist:
#         return Response({
#             'status': 'App not installed',
#         })
#
#     if app_store_id == 'io.re-public.streamr_node':
#
#         try:
#
#             streamr_container = client.containers.get('streamr-broker-node')
#
#             return Response({
#                 'status': streamr_container.status,
#             })
#
#         except docker.errors.NotFound:
#             return Response({
#                 'status': 'not running',
#             })
#
#     return Response({
#         'status': 'ok',
#         'app_store_id': app_store_id,
#     })