import paramiko


class SFTP(object):
    def __init__(self, hostname, username, password, port=22):
        self._sftp = None
        self._ssh_client = None
        self.username = username
        self.hostname = hostname
        self.port = port
        self.password = password

    def __enter__(self):
        self._ssh_client = paramiko.SSHClient()
        self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh_client.connect(hostname=self.hostname, port=self.port,
                                 username=self.username,
                                 password=self.password)

        self._sftp = sftp = self._ssh_client.open_sftp()

        return sftp

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._sftp is not None:
            self._sftp.close()
        if self._ssh_client is not None:
            self._ssh_client.close()
