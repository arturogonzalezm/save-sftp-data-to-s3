import os
import socket

import boto3

import paramiko

from sftp import SFTP


def lambda_handle(event, context):
    chunk_size = 12428800

    username = event['username']
    hostname = event['hostname']
    port = event.get('port') or 22
    ftp_dir = event['path']
    password = event['password']
    key_id = event['']
    key = event['']
    bucket_name = event['']
    s3_client = boto3.client('s3')

    try:
        with SFTP(hostname=hostname, username=username, password=password, port=port) as sftp:
            sftp.chdir(ftp_dir)
            for key in sftp.listdir():
                remote_file_path = os.path.join(ftp_dir, key)
                with sftp.file(remote_file_path, 'rb', bufsize=-1) as body:
                    response = s3_client.put_object(
                        body=body,
                        bucket=bucket_name,
                        key=key,
                    )
                    print(response)
    except (socket.error, paramiko.SSHException) as ex:
        return 'Failed to connect to {username}@{hostname}:{port}'.format(hostname=hostname, username=username,
                                                                          port=port)
