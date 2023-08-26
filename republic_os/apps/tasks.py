from celery import shared_task
import subprocess
import os
# import docker


# @shared_task(bind=True)
# def install_app(self, app):
#     print('Installing app: ', app)
#
#     os.makedirs('~/.streamrDocker1', exist_ok=True)
#
#     client = docker.from_env()
#
#     image_name = 'streamr/broker-node:latest'
#
#     image = client.images.pull(image_name)
#
#     # subprocess.run(['docker', 'pull', app['dockerImage']], check=True)
#
#     container_name = 'streamr-broker-node'
#
#     client.containers.run(image_name, detach=True, name=container_name)
#
#     # subprocess.run(['docker', 'run', '-d', '--name', container_name, image_name], check=True)
#
#     # Check if the Docker container is running
#     # result = subprocess.run(['docker', 'ps', '-f', f'name={container_name}'], stdout=subprocess.PIPE, text=True)
#     result = client.containers.list()
#
#     print(result)
#
#     return {
#         'result': 'App installed'
#     }