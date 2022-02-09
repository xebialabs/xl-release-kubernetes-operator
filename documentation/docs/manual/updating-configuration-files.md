---
sidebar_position: 6
---

# Updating configuration files

## Update xl-release.conf for Release xl-release.conf

Get current xl-release.conf file from the release server node:
```shell
❯ kubectl cp dai-xlr-digitalai-release-0:/opt/xebialabs/xl-release-server/conf/xl-release.conf ./xl-release.conf
```

Create following template file to append to it the retrieved `./xl-release.conf`:
```shell
❯ echo 'apiVersion: v1
kind: ConfigMap
metadata:
  name: xl-release-conf-config-map
  labels:
    app: digitalai-release
data:
  xl-release.conf: |' > config-patch-xl-release-conf.yaml.template
```

Merge the files:
```shell
❯ cat config-patch-xl-release-conf.yaml.template > config-patch-xl-release-conf.yaml
❯ sed -e 's/^/     /' xl-release.conf >> config-patch-xl-release-conf.yaml
```

Change the config in the `config-patch-xl-release-conf.yaml`.

Create the config map with `config-patch-xl-release-conf.yaml`:
```shell
❯ kubectl create -f config-patch-xl-release-conf.yaml
```

Get all statefulsets (release statefulset will be suffixed with `-release`):
```shell
❯ kubectl get sts -o name
```

Change the statefulset for the release server by adding volume mounts and volumes:
```shell
❯ kubectl get statefulset.apps/dai-xlr-digitalai-release -o yaml \
    | yq eval '.spec.template.spec.containers[0].volumeMounts += {
        "mountPath": "/opt/xebialabs/xl-release-server/conf/xl-release.conf",
        "name": "xl-release-conf-volume",
        "subPath": "xl-release.conf"
      }' - \
    | yq eval '.spec.template.spec.volumes += [{
        "name": "xl-release-conf-volume",
        "configMap": {
          "name": "xl-release-conf-config-map"
        }
      }]' - \
    | kubectl replace -f -
```

Restart Release servers (all release server pods):
```shell
❯ kubectl delete pod dai-xlr-digitalai-release-0
```

## Update configuration file generic example for Release

You can use following way to update any configuration file on the Release `conf` directory.

:::note
The files in the directory `conf` need to be updated on all replicated server nodes.
:::

Get info to list deploy master and worker pod names and statefulsets:
```shell
kubectl get pod -o name
kubectl get sts -o name
```

Setup environment vals:
- change `CONFIG_FILE` variable and `PATH_TO_CONFIG_FILE` to :
```shell
export PRODUCT=release
export POD_NAME=dai-xlr-digitalai-release-0
export CONFIG_FILE=xl-release.conf
export CONFIG_FILE_DASH=${CONFIG_FILE//./-}
export PATH_TO_CONFIG_FILE=/opt/xebialabs/xl-$PRODUCT-server/conf/$CONFIG_FILE
export STATEFUL_SET_NAME=statefulset.apps/dai-xlr-digitalai-release
```

Run set of commands:
```shell
kubectl cp $POD_NAME:$PATH_TO_CONFIG_FILE ./$CONFIG_FILE

echo "apiVersion: v1
kind: ConfigMap
metadata:
  name: $CONFIG_FILE_DASH-config-map
  labels:
    app: digitalai-$PRODUCT
data:
  $CONFIG_FILE: |" > config-patch-${CONFIG_FILE}.yaml.template
  
cat config-patch-${CONFIG_FILE}.yaml.template > config-patch-${CONFIG_FILE}.yaml
sed -e 's/^/     /' $CONFIG_FILE >> config-patch-${CONFIG_FILE}.yaml
```

Edit the YAML file and add your custom changes to it: `config-patch-${CONFIG_FILE}.yaml`

Create config map on cluster and use it:
```shell
kubectl create -f config-patch-${CONFIG_FILE}.yaml
kubectl get $STATEFUL_SET_NAME -o yaml \
    | yq eval ".spec.template.spec.containers[0].volumeMounts += {
        \"mountPath\": \"$PATH_TO_CONFIG_FILE\",
        \"name\": \"$CONFIG_FILE_DASH-volume\",
        \"subPath\": \"$CONFIG_FILE\"
      }" - \
    | yq eval ".spec.template.spec.volumes += [{
        \"name\": \"$CONFIG_FILE_DASH-volume\",
        \"configMap\": {
          \"name\": \"$CONFIG_FILE_DASH-config-map\"
        }
      }]" - \
    | kubectl replace -f -
kubectl delete pod $POD_NAME
```

### Upgrade process if you have updated files with config maps

To preserve configuration changes after upgrades, you will need to build custom images of the operator with all custom changes in
the statefulsets:
1. Checkout correct branch for the Release helm chart with the target version branch of the operator from here: [xl-release-kubernetes-helm-chart](https://github.com/xebialabs/xl-release-kubernetes-helm-chart)
2. Build the operator with the provided script in the root of the repo: `./build_operator.sh`
3. Release the operator to the image repository according to the script's guide
4. Use the newly created image as the answer during `xl op --upgrade` execution:
   - `Operator image to use (OperatorImageRelease)`
5. After the upgrade, if the upgrade changes the configuration files, transfer the changes to the config-map so the changes could be preserved.

## Update configuration file for RabbitMQ

To change configuration of the RabbitMQ use available parameters on the
[RabbitMQ packaged by Bitnami](https://github.com/bitnami/charts/tree/master/bitnami/rabbitmq#parameters)

## Update configuration file for PostgreSql

To change configuration of the PostgreSql use available parameters on the
[PostgreSQL packaged by Bitnami](https://github.com/bitnami/charts/tree/master/bitnami/postgresql#parameters)

## Upgrade process if you have updated the CR values

To preserve changed values in the CR use the following:
1. Download operator zip version from the [release operator zip](https://dist.xebialabs.com/customer/operator/release/)
with specific provider and version that you will install
2. Run `xl op --upgrade` with answers:
```
Do you want to use a custom operator zip file for Release? (UseOperatorZipRelease): Yes
Release operator zip to use (absolute path or URL to the zip) (OperatorZipRelease): [Path to the zip file that you downloaded]
Edit list of custom resource keys that will migrate to the new Release CR (PreserveCrValuesRelease): [Check comment below]
```
Add all paths where you updated CR values from the original value.
