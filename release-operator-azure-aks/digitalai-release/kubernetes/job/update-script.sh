#!/bin/bash

# ideally, xl-release.conf should come as input volume mount
cd /
kubectl cp dai-xlr-digitalai-release-0:/opt/xebialabs/xl-release-server/conf/xl-release.conf ./xl-release.conf
kubectl get configMap xl-release-conf-config-map -o yaml > ./config-patch-xl-release-conf.yaml
sed -e 's/^/     /' xl-release.conf >> config-patch-xl-release-conf.yaml
kubectl apply -f config-patch-xl-release-conf.yaml
kubectl get statefulset.apps/dai-xlr-digitalai-release -o yaml \
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
