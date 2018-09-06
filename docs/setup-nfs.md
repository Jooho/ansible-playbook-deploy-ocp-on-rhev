Setup NFS Server
----------------

## 1. Download ansible galaxy role
ansible-galaxy install -f -r requirements.yaml -p ./roles

## 2. Update variable
```
vi vars/all

nstall: true
nfs_target_vm: infra_node
nfs_mount_point: /exports
nfs_block_dev_name: /dev/sdc
```



