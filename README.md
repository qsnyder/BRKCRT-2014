# BRKCRT-2014

This repository will serve as the collection point of the code samples demonstrated in BRKCRT-2014 at CLUS 2023 in Las Vegas.  While this README is a (nearly) complete how-to on how to use the code, it may become dated as exam requirements change due to natural revisions.

## Requirements

- (IOSXE on CSR Latest Code with ZTP Functionality)[https://devnetsandbox.cisco.com/RM/Diagram/Index/aa067fb8-159f-4d0c-8339-a86074a3ea01] sandbox from DevNet Sandbox
- Ability to VPN to DevNet Sandbox using Anyconnect or Openconnect
- Workstation with recently current version of Python (Python 3.6+)
- Python PIP installed

## Clone Code; Building the Virtual Environment

Best practice dictates that we should use a virtual environment to isolate the dependencies of this code from our system.  Lets do so by cloning the code, and creating a virtual environment within the folder.

```bash
git clone https://github.com/qsnyder/BRKCRT-2014.git
cd BRKCRT-2014/
python -m venv brkcrt2014
```

> It may be necessary on your system to change `python` to `python3` in the above code block

Next, we'll activate the virtual environment and install the dependencies

```bash
source brkcrt2014/bin/activate
pip install -r requirements.txt
```

> It may be necessary to use `pip3` rather than `pip` on your system

Once you are connected to the DevNet Sandbox via VPN, you are now ready to use the code.

## RESTCONF Python Script

Move into the directory containing the Python code

```bash
cd restconf-requests
```

From there, we can either look at the code, or simply execute it by invoking the Python command

```bash
python interface-restconf-config-verify.py
```

This will print the JSON-encoded output of the current configuration on the interface, make a change to the description of that interface, and then print the resulting configuration after the change.

### Sample Output

```json
{
  "Cisco-IOS-XE-native:GigabitEthernet": {
    "name": "2",
    "description": "Network Interface",
    "shutdown": [null],
    "mop": {
      "enabled": false,
      "sysid": false
    },
    "Cisco-IOS-XE-ethernet:negotiation": {
      "auto": true
    }
  }
}


{
  "Cisco-IOS-XE-native:GigabitEthernet": {
    "name": "2",
    "description": "Description updated by RESTCONF",
    "shutdown": [null],
    "mop": {
      "enabled": false,
      "sysid": false
    },
    "Cisco-IOS-XE-ethernet:negotiation": {
      "auto": true
    }
  }
}
```

## Ansible SNMP Configuration Change

Return to the root of this repository (if needed) and move to the `ansible` folder

```bash
cd ../
cd ansible
```

Within this folder, there are several files that determine how Ansible will operate when a playbook is executed from this folder.

### `ansible.cfg`

The key points to this file are that the `inventory` file location has been set (meaning that the `-i` flag to indicate inventory file will not be required when running `ansible-playbook` commands) and that the collection location will be contained within the `BRKCRT-2014/ansible` folder, rather than installed within your home directory.  These lines are given by 

```ini
[defaults]
host_key_checking = False
inventory      = ./inventory.ini
roles_path     = ./roles
collections_path = ./collections
```

### `inventory.ini`

This file defines the host that we will connect to (a CSR1000v) using a given name of our choosing, its IP address, and the OS on which it is running.  The username and password are also defined in this file which will allow Ansible to connect to the device using SSH methods (either `paramiko` or `ansible-pylibssh`, depending on what is installed).

```ini
[iosxe]
csr1 ansible_host=10.10.20.48 ansible_network_os=cisco.ios.ios

[all:vars]
ansible_user=developer
ansible_ssh_pass=C1sco12345
ansible_connection=network_cli
```

### Usage

Prior to running the playbook, the Cisco IOS Ansible collection will need to be installed from Ansible Galaxy.  This change was required as of Ansible 2.10 and is a required step, as without it, Ansible will not have the required modules to make the changes to the CSR1000v device.

```bash
ansible-galaxy collection install cisco.ios
```

You should now see a folder called `collections` within the current `ansible` folder.

To run the playbook, simply invoke the following command from the shell of your workstation

```bash
ansible-playbook pb-configure-snmp.yaml
```

If so desired, you can append a verbosity level to the end of the command using one or more `v`s like `-v` or `-vv`

> Note: This playbook has been written in the new Ansible module syntax, using the state declarative modules for Cisco IOS, which may be different from previous versions of this playbook using `ios_config` or so.

### Sample Output

```
[brkcrt2014] ansible [main] » ansible-playbook pb-configure-snmp.yaml -v
Using /Users/qsnyder/dev/BRKCRT-2014/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] *********************************************************************************************************************************

TASK [TASK 1 in PLAY 1 - Modifying the SNMP configuration] ***************************************************************************************************************************
changed: [csr1] => {"after": {"communities": [{"name": "CLUS-DEMO", "ro": true}], "contact": "BEARDED_GUY", "location": "LAS_VEGAS"}, "before": {}, "changed": true, "commands": ["snmp-server contact BEARDED_GUY", "snmp-server location LAS_VEGAS", "snmp-server community CLUS-DEMO ro"]}

TASK [TASK 2 in PLAY 1 - Verify the SNMP configuration exists] ***********************************************************************************************************************
ok: [csr1] => {"changed": false, "gathered": {"communities": [{"name": "CLUS-DEMO", "ro": true}], "contact": "BEARDED_GUY", "location": "LAS_VEGAS"}}

PLAY RECAP ***************************************************************************************************************************************************************************
csr1                       : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Questions, Comments, Feedback

For any questions, please reach out to me on Twitter via DM @qsnyder
