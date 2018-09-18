Add a PV to Service Catalog(Ansible-Service-Broker)
-------------------------------------------------

After OCP installtion, you can see Ansible Service Broker use wrong name of PV.
```
$ oc get pvc
NAME      STATUS    VOLUME              CAPACITY   ACCESSMODES   STORAGECLASS   AGE
etcd      Bound      prometheus-volume   0                                       7h
```

So you will fix it!

## Steps
*Delete existing PV*
```
oc delete pvc etcd -n openshift-ansible-service-broker
```


*Create a new PVC*
```
echo "apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: etcd
  namespace: openshift-ansible-service-broker
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1G"| oc create -f -
```

*Redeploy all pods*
```
oc rollout latest dc/asb-etcd -n openshift-ansible-service-broker
oc rollout latest dc/asb -n openshift-ansible-service-broker
```


## Result 
```
$ oc get pv,pvc,pod -n openshift-ansible-service-broker
NAME                                          CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM                                       STORAGECLASS          REASON    AGE
pv/pvc-91b8762b-b697-11e8-a31a-021a4a0ab219   1G         RWO           Delete          Bound     openshift-ansible-service-broker/etcd       managed-nfs-storage             1m

NAME       STATUS    VOLUME                                     CAPACITY   ACCESSMODES   STORAGECLASS          AGE
pvc/etcd   Bound     pvc-91b8762b-b697-11e8-a31a-021a4a0ab219   1G         RWO           managed-nfs-storage   1m

NAME                   READY     STATUS              RESTARTS   AGE
po/asb-2-nmzj4        1/1       Running       0          1m
po/asb-etcd-2-qgtq9   1/1       Running       0          1m
```
