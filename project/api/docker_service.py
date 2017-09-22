import os

from docker import APIClient


client = APIClient()


def create_container(code, container_name):
    client.create_container(
        image='python:latest',
        command=['/usr/bin/python', '-c', code.getvalue()],
        volumes=['/opt'],
        host_config=client.create_host_config(
            binds={
                os.getcwd(): {
                    'bind': '/opt',
                    'mode': 'rw',
                }
            }
        ),
        name=container_name,
        working_dir='/opt'
    )
    return True


def get_output(container_name):
    client.start(container_name)
    client.wait(container_name)
    output = client.logs(container_name)
    client.remove_container(container_name, force=True)
    return output
