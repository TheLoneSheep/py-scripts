import paramiko
from pathlib import Path
import os


servers = ['192.168.0.1', '192.168.1.1']

modules = ['module1',
           'module2',
           'module3',
           'module4',
           'module5',
           'module6']


def connect_ssh_and_get_logs(host, path, file):
    client = paramiko.SSHClient()  # initialize SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect with ssh
    client.connect(hostname=host, username='admin', password='admin',
                   look_for_keys=False, allow_agent=False)

    sftp = client.open_sftp()   # open sftp connection

    # download files from the provided list
    sftp.get(remotepath=f'/var/log/{file}.log',
             localpath=os.path.abspath(Path(path / (file + '.log'))))

    sftp.close()    # close sftp
    client.close()  # close SSHClient


def main(hosts, files):
    # create Download folder if it doesn't exist already
    cwd = os.path.abspath(Path.cwd())
    download = Path(Path(cwd) / 'Download')
    if not Path.exists(download):
        Path(download).mkdir()

    for host in hosts:
        host_path = Path(download / f'{host}')
        if not Path.exists(host_path):
            Path(host_path).mkdir()

        # os.chdir(Path.cwd() / f'{host}')
        for file in files:
            connect_ssh_and_get_logs(host, host_path, file)


main(servers, modules)
input('Done. Press Enter to exit..')

