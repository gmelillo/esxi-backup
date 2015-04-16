from paramiko import SSHClient, AutoAddPolicy
from re import search
from urllib import urlretrieve
from time import strftime
from easywebdav import connect as webdav_connect
import logging
from config import ConfigurationINI, get_config_path
from socket import error as SocketError

logging.basicConfig(level=logging.DEBUG)

config = ConfigurationINI(get_config_path(__file__, '/esxi.ini'))
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

LINK = None

for l in stdout:
    #m = search('(\/downloads\/[0-9a-zA-Z\-]+\/configBundle\-.*)', l.strip())
    m = search('http://\*(.*)', l.strip())
    if m is not None:
        download = "http://{host}{position}".format(
            host=config['esxi']['hostip'],
            position=m.group(1)
        )
        logging.info("Downloading {}".format(download))
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
            comediaoc.upload(local_file, '{}/backup-{}-{}.tgz'.format(
                config['webdav']['savepath'],
                config['esxi']['hostdns'],
                strftime(config['local']['dateformat'])
            ))

ssh.close()
