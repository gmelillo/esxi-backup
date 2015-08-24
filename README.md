# esxi-backup
Export vmware configuration and store it on webdav server


## Setup with virtualenv

### Download source and prepare the virtual enviroment :

```bash
yum install gcc python-virtualenv
cd /opt
git clone git@github.com:gmelillo/esxi-backup.git && cd esxi-backup.git
virtualenv esxi && source esxi/bin/activate
pip install -r requirements.txr
python setup.py install
deactivate
```

After setup you will be able to use ```bash /opt/esxi-backup/esxi/bin/esxi-backup``` backup the hypervisor described in ```bash /etc/esxi.ini```
