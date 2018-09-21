Script
```
mkdir OFT;cd OFT

git clone git@github.com:Jooho/ansible-playbook-deploy-ocp-on-rhev.git  

cd ansible-playbook-deploy-ocp-on-rhev

git checkout -b 3.7 origin/3.7

openssl s_client -connect lab-rhevm-2.gsslab.rdu2.redhat.com:443 -showcerts -servername lab-rhevm-2.gsslab.rdu2.redhat.com -verify 5

vi ~/rhev.crt

vi ~/setup-jooho
```
Credential
~~~
# RHEV(upstream name: Ovirt) Information
export OVIRT_USERNAME=USER@Profile
export OVIRT_PASSWORD=
export OVIRT_URL=https://X.X.redhat.com/ovirt-engine/api
export OVIRT_CA_PATH=/root/rhev.crt


# Base Image Credential Information
export BASE_IMAGE_ID=root
export BASE_IMAGE_PW=redhat

# Red hat subscription manager information
export RHSM_ID=''
export RHSM_PW=''

# Subscription Name or Pool ID (If both set, Pool ID has more priority)
export BROKER_SUB_POOL="Red Hat OpenShift Container Platform Broker/Master Infrastructure
export NODE_SUB_POOL="Red Hat OpenShift Container Platform, Standard, 2-Core"
export BROKER_SUB_POOL_ID="XXXXXXX"
export NODE_SUB_POOL_ID="XXXXXXX"
~~~

```
source setup


inventory/rhev/hosts/ovirt.py --pretty    

  
./deploy.py --deploy_type=ansible-controller  --operate=create     ==> 8min


ssh ansible-controller

export AC=insights-content.prod.gsslab.rdu2.redhat.com
scp ~/setup root@$AC:/root/. 
scp ~/rhev.crt root@$AC:/root/. 

ssh root@$AC

cd git/ansible-playbook-deploy-ocp-on-rhev/

source ~/setup
git checkout -b 3.7 origin/3.7


vi vars/all    ==> change nfs ip  /dev

ansible-galaxy install -f -r requirements.yaml -p ./roles

ssh-copy-id -i ~/.ssh/id_rsa.pub $(hostname)

./deploy.py --deploy_type=nfs -vvv  ==> 2 hours


mkdir /exports-nfs/registry
```

