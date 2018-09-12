Prometheus Component
---------------------------

*Features*
- Deploy
- Undeploy

### Deploy Prometheus During OCP Installation ####

Edit vars/ocp_param then install OCP cluster.
```
# Prometheus
openshift_hosted_prometheus_deploy: true
openshift_prometheus_node_selector: {"region": "app"}
openshift_prometheus_storage_kind: nfs
openshift_prometheus_storage_access_modes: ['ReadWriteOnce']
openshift_prometheus_storage_host: "{{nfs_server_ip}}"
openshift_prometheus_storage_nfs_directory: "{{nfs_mount_point}}"
openshift_prometheus_storage_volume_name: prometheus
openshift_prometheus_storage_volume_size: 5Gi
#openshift_prometheus_storage_labels: {'storage': 'prometheus'}
openshift_prometheus_storage_type: 'pvc'
openshift_prometheus_storage_class: managed-nfs-storage
# For prometheus-alertmanager
openshift_prometheus_alertmanager_storage_kind: nfs
openshift_prometheus_alertmanager_storage_access_modes: ['ReadWriteOnce']
openshift_prometheus_alertmanager_storage_host: "{{nfs_server_ip}}"
openshift_prometheus_alertmanager_storage_nfs_directory: "{{nfs_mount_point}}"
openshift_prometheus_alertmanager_storage_volume_name: prometheus-alertmanager
openshift_prometheus_alertmanager_storage_volume_size: 5Gi
#openshift_prometheus_alertmanager_storage_labels: {'storage': 'prometheus-alertmanager'}
openshift_prometheus_alertmanager_storage_type: 'pvc'
openshift_prometheus_alertmanager_storage_class: managed-nfs-storage
# For prometheus-alertbuffer
openshift_prometheus_alertbuffer_storage_kind: nfs
openshift_prometheus_alertbuffer_storage_access_modes: ['ReadWriteOnce']
openshift_prometheus_alertbuffer_storage_host: "{{nfs_server_ip}}"
openshift_prometheus_alertbuffer_storage_nfs_directory: "{{nfs_mount_point}}"
openshift_prometheus_alertbuffer_storage_volume_name: prometheus-alertbuffer
openshift_prometheus_alertbuffer_storage_volume_size: 5Gi
#openshift_prometheus_alertbuffer_storage_labels: {'storage': 'prometheus-alertbuffer'}
openshift_prometheus_alertbuffer_storage_type: 'pvc'
openshift_prometheus_alertbuffer_storage_class: managed-nfs-storage

```

### Deploy Prometheus After OCP Installation ###
```
./deploy.py --deploy_type=prometheus --operate=deploy
```

### Undeploy Prometheus ###

```
./deploy.py --deploy_type=promethues --operate=undeploy
```


### ETC ###
- [Attach PV to Prometheus](./prometheus_pv.md)
