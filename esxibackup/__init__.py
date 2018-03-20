from paramiko import SSHClient, AutoAddPolicy
from re import search
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve
from time import strftime
from easywebdav import connect as webdav_connect
import logging
from sys import version_info
from socket import error as SocketError
from os.path import isfile
if version_info >= (3, 0):
    from .config import ConfigurationINI, get_config_path
else:
    from config import ConfigurationINI, get_config_path


def main():
    logging.basicConfig(level=logging.INFO)

    if isfile(get_config_path(__file__, '/esxi.ini')):
        config = ConfigurationINI(get_config_path(__file__, '/esxi.ini'))
    elif isfile('/etc/esxi.ini'):
        config = ConfigurationINI('/etc/esxi.ini')
    else:
        logging.critical('/etc/esxi.ini missing.')
        exit(0)

    logging.debug('Configuration file used : {conf}'.format(conf=get_config_path(__file__, '/esxi.ini')))

    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(config['esxi']['hostip'], username=config['esxi']['username'], password=config['esxi']['password'])
    except SocketError as e:
        logging.critical('Host unreachable.')
        logging.critical(e.__str__())
        exit()

    logging.info('vim-cmd hostsvc/firmware/sync_config')
    ssh.exec_command('vim-cmd hostsvc/firmware/sync_config')
    logging.info('vim-cmd hostsvc/firmware/backup_config')
    stdin, stdout, stderr = ssh.exec_command('vim-cmd hostsvc/firmware/backup_config')

    for l in stdout:
        m = search('http://\*(.*)', l.strip())
        if m is not None:
            download = "http://{host}{position}".format(
                host=config['esxi']['hostip'],
                position=m.group(1)
            )
            logging.info("Downloading {0}".format(download))
            local_file = '{localpath}/backup-{host}-{date}.tgz'.format(
                host=config['esxi']['hostdns'],
                date=strftime(config['local']['dateformat']),
                localpath=config['local']['savepath']
            )
            urlretrieve(download, local_file)

            if config['webdav']['enabled']:
                logging.info("Uploading file on WebDAV")
                comediaoc = webdav_connect(
                    config['webdav']['host'],
                    username=config['webdav']['username'],
                    password=config['webdav']['password'],
                    protocol=config['webdav']['proto'],
                    verify_ssl=False
                )
                comediaoc.upload(local_file, '{0}/backup-{1}-{2}.tgz'.format(
                    config['webdav']['savepath'],
                    config['esxi']['hostdns'],
                    strftime(config['local']['dateformat'])
                ))
                logging.info('Cleaning old configurations')
                files = [file for file in comediaoc.ls(config['webdav']['savepath']) if file.contenttype == 'application/x-compressed']

    ssh.close()

if __name__ == '__main__':
    main()
