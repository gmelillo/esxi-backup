[![Build Status](https://travis-ci.org/gmelillo/esxi-backup.svg?branch=master)](https://travis-ci.org/gmelillo/esxi-backup)

# esxi-backup
Export vmware configuration and store it on webdav server

## Setup with virtualenv

```bash
yum install gcc python-virtualenv
cd /opt
git clone git@github.com:gmelillo/esxi-backup.git && cd esxi-backup.git
virtualenv esxi && source esxi/bin/activate
pip install -r requirements.txr
python setup.py install
deactivate
```

After setup you will be able to use ```/opt/esxi-backup/esxi/bin/esxi-backup``` backup the hypervisor described in ```/etc/esxi.ini```

## Restore

```
vim-cmd hostsvc/maintenance_mode_enter
vim-cmd hostsvc/firmware/restore_config /path/to/backup/file

```

### [Additional info](https://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2042141)

**Note:** The information about virtual machines is not stored in the config backup and the virtual machines must be re-inventoried from the datastore browser after a config backup restore. Also, bootbank information is not stored in a config backup. If needed, this must be backed up and downloaded separately in a compressed tar file.

For more information, see:
  - Backing Up Configuration Information with vicfg-cfgbackup section in the [vSphere 5.1 Command Line Documentation](http://pubs.vmware.com/vsphere-51/topic/com.vmware.vcli.examples.doc/cli_manage_hosts.4.4.html)
  - Get-VMHostFirmware section in the [vSphere PowerCLI Reference](http://pubs.vmware.com/vsphere-51/topic/com.vmware.powercli.cmdletref.doc/Get-VMHostFirmware.html)
  - Set-VMHostFirmware section in the [vSphere PowerCLI Reference](http://pubs.vmware.com/vsphere-51/topic/com.vmware.powercli.cmdletref.doc/Set-VMHostFirmware.html)

**Note:** if you have installed  a version of vSphere later than 5.1, see the Command Line Document and PowerCLI Reference for that version in the VMware Documentation Library.

**PowerCLI Notes:**
  - Remember that the 64 bit version of PowerCLI is installed in C:\Program Files, and the 32 bit version is in C:\Program Files (x86).
  - You must always run PowerCLI as Administrator.
