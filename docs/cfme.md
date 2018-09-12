CFME Component
---------------------------

*Features*
- Deploy
- Undeploy

### Deploy CFME During OCP Installation ####

Edit vars/ocp_param then install OCP cluster.
```
# CFME project
openshift_management_project: openshift-management
openshift_management_project_description: CloudForms Management Engine
openshift_management_app_template: cfme-template
openshift_management_storage_class: nfs_external
openshift_management_install_beta: true
openshift_management_template_parameters: {'APPLICATION_MEM_REQ': '3000Mi', 'POSTGRESQL_MEM_REQ': '1Gi', 'ANSIBLE_MEM_REQ': '512Mi', 'APPLICATION_VOLUME_CAPACITY': '5Gi', 'DATABASE_VOLUME_CAPACITY': '10Gi'}
openshift_management_storage_nfs_external_hostname: "{{nfs_server_ip}}"
openshift_management_storage_nfs_base_dir: "{{nfs_mount_point}}"

```

### Deploy CFME After OCP Installation ###
```
./deploy.py --deploy_type=cfme --operate=deploy
```

### Undeploy CFME ###

```
./deploy.py --deploy_type=cfme --operate=undeploy
```


### Post Installation ###
- Delete PVs(we will use StorageClass)
```
$ oc get pv
NAME                                       CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS      CLAIM                                                 STORAGECLASS          REASON    AGE
cfme-app                                   5Gi        RWO           Retain          Available                                                                                         7m
cfme-db                                    10Gi       RWO           Retain          Available                                                                                         7m
pvc-ecd2db6a-b69d-11e8-a31a-021a4a0ab219   10Gi       RWO           Delete          Bound       openshift-management/cloudforms-postgresql            managed-nfs-storage             7m
pvc-ed742d0c-b69d-11e8-a31a-021a4a0ab219   5Gi        RWO           Delete          Bound       openshift-management/cloudforms-server-cloudforms-0   managed-nfs-storage             7m

$ oc delete pv cfme-app cfme-db
```
