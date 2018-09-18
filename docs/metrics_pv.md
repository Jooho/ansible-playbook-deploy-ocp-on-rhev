Attach PV to Metrics
--------------------

After OCP installation, you can see wrong PV is attached to Metric cassandra.
```
[root@dhcp182-21 nfs-client-provisioner]# oc get pv
NAME                                       CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS      CLAIM                                       STORAGECLASS          REASON    AGE
prometheus-alertbuffer-volume              5Gi        RWO           Retain          Available                                                                               7h
prometheus-alertmanager-volume             5Gi        RWO           Retain          Released    openshift-infra/metrics-cassandra-1                                         7h
prometheus-volume                          5Gi        RWO           Retain          Bound       openshift-ansible-service-broker/etcd                                       7h
```
So we need to fix it.

## Steps
* Delete existing pv,pvc
- PV related with prometheus do not need anymore because new PVs for it are already created by dynamic PV(Storage Class)
- PVC for metrics will be replaced with new PVC
```
oc delete pvc metrics-cassandra-1 -n openshift-infra

oc delete pv prometheus-alertmanager-volume prometheus-alertbuffer-volume prometheus-volume
```

* Create new pvc
```
echo "apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  annotations:
  labels:
    metrics-infra: hawkular-cassandra
  name: metrics-cassandra-1
  namespace: openshift-infra
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi"|oc create -f -
```

* Restart all pods
```
oc delete pod --all
```




