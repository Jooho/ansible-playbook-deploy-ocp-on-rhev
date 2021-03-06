Ansible Controller VM
---------------------

*Description*

  This help create RHEV VM from base template and it will install essential packages/git repositories.
  For deploying openshift cluster, you should create Ansible Controller. Moreover, 

*Files*
- playbooks/rhev/ansible-controller.yaml

*Pre-requisites*
- [Create base rhel image](./base-rhel-image.md)
- [Create ocp base template](./base-rhel-ocp-template.md)

*Related Docs*
- [Download RHEV Cert](./download-rhev-cert.md)
- [Credential Information](./setup.md)


*Manaual Way*
```
yum install ansible -y

wget https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
chmod 777 /tmp/get-pip.py
python /tmp/get-pip.py
pip install ovirt-engine-sdk-python 

```

*Ansible Way*

**Create Ansible Controller VM**

```
 ./deploy.py --deploy_type=ansible-controller --operate=install
```
**Config Ansible Controller on the VM where you are on**

```
 ./deploy.py --deploy_type=ansible-controller --operate=config
```

*Video Clips:*

[![asciicast](https://asciinema.org/a/142052.png)](https://asciinema.org/a/142052)
[![asciicast](https://asciinema.org/a/142059.png)](https://asciinema.org/a/142059)
