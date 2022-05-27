#!/bin/bash

wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
chmod a+x /usr/local/bin/yq

apk update
apk add curl

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

#kubectl cp dai-ocp-xlr-digitalai-release-ocp-0:/opt/xebialabs/xl-release-server/conf/xl-release.conf ./xl-release.conf
kubectl exec -ti dai-ocp-xlr-digitalai-release-ocp-0 -- cat conf/xl-release.conf > xl-release.conf
kubectl create cm xl-release-conf-config-map --from-file=xl-release.conf
kubectl get statefulset.apps/dai-ocp-xlr-digitalai-release-ocp -o yaml \
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
