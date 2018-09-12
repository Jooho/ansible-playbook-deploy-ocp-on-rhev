Service Catalog Component
---------------------------

*Features*
- Deploy
- Undeploy

### Deploy Service Catalog During OCP Installation ####

Edit vars/ocp_param then install OCP cluster.
```
# Enable service catalog
openshift_enable_service_catalog: true

# Service broker
template_service_broker_install: true

# TSB node selector
template_service_broker_selector: {'region': 'infra'}
# Force a specific prefix (IE: registry) to use when pulling the service catalog image
# NOTE: The registry all the way up to the start of the image name must be provided. Two examples
# below are provided.
#openshift_service_catalog_image_prefix: docker.io/openshift/origin-
#openshift_service_catalog_image_prefix: registry.access.redhat.com/openshift3/ose-
# Force a specific image version to use when pulling the service catalog image
#openshift_service_catalog_image_version: v3.7

# Configure one of more namespaces whose templates will be served by the TSB
#openshift_template_service_broker_namespaces: ['openshift']

# masterConfig.volumeConfig.dynamicProvisioningEnabled, configurable as of 1.2/3.2, enabled by default
#openshift_master_dynamic_provisioning_enabled: False


```

### Deploy Service Catalog After OCP Installation ###
```
./deploy.py --deploy_type=service_catalog --operate=deploy
```

### Undeploy Service Catalog ###

```
./deploy.py --deploy_type=promethues --operate=undeploy
```


### ETC ###
- [Attach PV to Service Catalog](./service_catalog_pv.md)
