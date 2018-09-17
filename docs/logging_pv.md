Attach PV to Logging Stack
-------------------------

After OCP installation, you can see Elastic Search pod failed to deploy because of PV.
```
$ oc get pod
NAME                                       READY     STATUS    RESTARTS   AGE
logging-es-data-master-fu3mz5p4-1-deploy   0/1       Error     0          7h

$ oc get pvc
NAME           STATUS    VOLUME    CAPACITY   ACCESSMODES   STORAGECLASS   AGE
logging-es-0   Pending                                                     7h
```

So we will fix it.


## Steps
*Delete existing pvc*

```
oc delete pvc --all -n logging
```

*Create a new PV*
```
echo "apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  labels:
    logging-infra: support
  name: logging-es-0
  namespace: logging
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi"|oc create -f -
```

*Deploy Elastic Search*
```
oc get dc -o name -n logging |grep es | xargs oc rollout cancel 
oc get dc -o name -n logging |grep es | xargs oc rollout latest 
oc get dc -o name -n logging |grep kibana |xargs oc rollout latest

oc delete pod -l component=fluend -n logging
```

## Results
```
$ oc get pod -w -n logging
NAME                                      READY     STATUS    RESTARTS   AGE
logging-es-data-master-fu3mz5p4-2-2t7sf   2/2       Running   0          54s

$ oc get pv -n logging
NAME                                       CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM                                       STORAGECLASS          REASON    AGE
pvc-aa25b057-b695-11e8-a31a-021a4a0ab219   5Gi        RWO           Delete          Bound     logging/logging-es-0                        managed-nfs-storage             7m

$ oc get pvc -n logging
NAME           STATUS    VOLUME                                     CAPACITY   ACCESSMODES   STORAGECLASS          AGE
logging-es-0   Bound     pvc-aa25b057-b695-11e8-a31a-021a4a0ab219   5Gi        RWO           managed-nfs-storage   7m

```


## Issues
registry.access.redhat.com/openshift3/logging-fluentd:v3.9.41 has issues so change it to image: registry.access.redhat.com/openshift3/logging-fluentd:v3.9.40

```
oc edit ds logging-fluetd
..
image: registry.access.redhat.com/openshift3/logging-fluentd:v3.9.40
...
```

