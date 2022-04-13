---
sidebar_position: 10
---

# How to change namespace in case there is release already running in the default namespace

## Prerequisites
- The kubectl command-line tool
- Access to a Kubernetes cluster with installed Release in the `default` namespace

Tested with:
- xl-deploy 10.3.9
- xl-release 10.3.9
- xl-cli 10.3.9
- Azure cluster

If you have already setup of the XLR default namespace it is possible to move the deployment to the custom namespace. Here we will use for example 
`custom-namespace-1`.

In the example we will use XLR 10.3 version with latest 10.3 operator image 10.3.0-407.1129 from the 
[https://hub.docker.com/r/xebialabsunsupported/release-operator/tags](https://hub.docker.com/r/xebialabsunsupported/release-operator/tags) and latest operator 
package from the 10.3 branch.

## Steps to setup operator on the custom namespace

With following steps you will setup XLR in the custom namespace, in parallel with running current setup in the `default` namespace.

### 1. Create custom namespace

Setup custom namespace on Kubernetes cluster, `custom-namespace-1` for example:
```
❯ kubectl create namespace custom-namespace-1
```

Replace `custom-namespace-1` name in this and following steps with your custom namespace name.

### 3. Prepare the release operator 

1. Get the release operator package zip for Azure: release-operator-azure-aks-10.3.0-407.1129.zip (operator image is already setup in the package).
2. Unzip the zip with the release operator package.
3. Collect all custom changes that are done in the `default` namespace for XLR resources
    - StatefulSets
    - Deployments
    - ConfigMaps
    - Secrets
    - CustomResource
    - anything else that was customized
4. Collect any other change that was done during initial setup according to the 
[https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#installing-deploy-on-azure-kubernetes-service](https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#installing-deploy-on-azure-kubernetes-service)
5. If you are using your own database and messaging queue setup, setup it in the same way as in the `default` namespace, 
in the new CR in the release operator package `digitalai-release/kubernetes/dairelease_cr.yaml`.
6. Apply all collected changes from the `default` namespace to the CR in the release operator package `digitalai-release/kubernetes/dairelease_cr.yaml`. 
(The best is to compare new CR `digitalai-release/kubernetes/dairelease_cr.yaml` with the one from the `default` namespace)

:::note
Note:
Any data migration is out of scope of this document. For example in case of database data migration, check with your DB admins what to do in that case.
:::

:::note
Note:
Check if configuration on the new namespace is using same host as on `default` namespace. 
In that case you will need to execute step 9.a to be able to access XLR pages.
:::

:::note
Note:
It would the best that XLR version remains the same as on `default` namespace (to avoid any additional changes in the XLR).
Compare values in the CR path `spec.ImageTag` and match them to the `default` namespace value.  
:::

### 5. Update the release operator package to support custom namespace (common part)

Update following files (relative to the provider's directory) with custom namespace name:

| File name                                                                  | Yaml path                                     | Value to set                                        |
|:---------------------------------------------------------------------------|:----------------------------------------------|:----------------------------------------------------|
| digitalai-release/infrastructure.yaml                                      | spec[0].children[0].children[0].name          | custom-namespace-1                                  |
| digitalai-release/infrastructure.yaml                                      | spec[0].children[0].children[0].namespaceName | custom-namespace-1                                  |
| digitalai-release/environment.yaml                                         | spec[0].children[0].members[0]                | ~Infrastructure/k8s-infra/xlr/custom-namespace-1    |
| digitalai-release/kubernetes/template/cluster-role-digital-proxy-role.yaml | metadata.name                                 | custom-namespace-1-xlr-operator-proxy-role          |
| digitalai-release/kubernetes/template/cluster-role-manager-role.yaml       | metadata.name                                 | custom-namespace-1-xlr-operator-manager-role        |
| digitalai-release/kubernetes/template/cluster-role-metrics-reader.yaml     | metadata.name                                 | custom-namespace-1-xlr-operator-metrics-reader      |
| digitalai-release/kubernetes/template/leader-election-rolebinding.yaml     | subjects[0].namespace                         | custom-namespace-1                                  |
| digitalai-release/kubernetes/template/manager-rolebinding.yaml             | metadata.name                                 | custom-namespace-1-xlr-operator-manager-rolebinding |
| digitalai-release/kubernetes/template/manager-rolebinding.yaml             | roleRef.name                                  | custom-namespace-1-xlr-operator-manager-role        |
| digitalai-release/kubernetes/template/manager-rolebinding.yaml             | subjects[0].namespace                         | custom-namespace-1                                  |
| digitalai-release/kubernetes/template/proxy-rolebinding.yaml               | metadata.name                                 | custom-namespace-1-xlr-operator-proxy-rolebinding   |
| digitalai-release/kubernetes/template/proxy-rolebinding.yaml               | roleRef.name                                  | custom-namespace-1-xlr-operator-proxy-role          |
| digitalai-release/kubernetes/template/proxy-rolebinding.yaml               | subjects[0].namespace                         | custom-namespace-1                                  |


In the `digitalai-release/applications.yaml` delete array element from the `spec[0].children[0].deployables`, where name is `name: custom-resource-definition`.
This will not deploy again CRD, as it already exists, when it was deployed for the first time. Example of the element to delete
```yaml
- name: custom-resource-definition
  type: k8s.ResourcesFile
  fileEncodings:
    ".+\\.properties": ISO-8859-1
  mergePatchType: strategic
  propagationPolicy: Foreground
  updateMethod: patch
  createOrder: 1
  modifyOrder: 2
  destroyOrder: 3
  displayResourceOnLogs: "false"
  showContainerLogs: "false"
  bytesToReadFromContainerLogs: 4000
  file: !file kubernetes/template/custom-resource-definition.yaml
```

### 6.a. Update the release operator package to support custom namespace - only in case of Nginx ingress controller

Following changes are in case of usage nginx ingress (default behaviour):

| File name                                       | Yaml path                                             | Value to set                                        |
|:------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------|
| digitalai-release/kubernetes/dairelease_cr.yaml | spec.ingress.annotations.kubernetes.io/ingress.class  | nginx-custom-namespace-1-dai-xlr                    |
| digitalai-release/kubernetes/dairelease_cr.yaml | spec.nginx-ingress-controller.extraArgs.ingress-class | nginx-custom-namespace-1-dai-xlr                    |
| digitalai-release/kubernetes/dairelease_cr.yaml | spec.nginx-ingress-controller.fullnameOverride        | custom-namespace-1-dai-xlr-nginx-ingress-controller |
| digitalai-release/kubernetes/dairelease_cr.yaml | spec.nginx-ingress-controller.ingressClass            | nginx-custom-namespace-1-dai-xlr                    |


### 6.b. Update the release operator package to support custom namespace - only in case of Haproxy ingress controller

:::note
Note:
To setup haproxy instead of default nginx configuration that is provided in the operator package you need to do following changes in the
`digitalai-release/kubernetes/dairelease_cr.yaml`:
- `spec.haproxy-ingress.install = true`
- `spec.nginx-ingress-controller.install = false`
- `spec.ingress.path = "/xl-release/"`
- in the `spec.ingress.annotations` replace all `nginx.` settings and put:
```
      kubernetes.io/ingress.class: "haproxy"
      ingress.kubernetes.io/ssl-redirect: "false"
      ingress.kubernetes.io/rewrite-target: /
      ingress.kubernetes.io/affinity: cookie
      ingress.kubernetes.io/session-cookie-name: JSESSIONID
      ingress.kubernetes.io/session-cookie-strategy: prefix
      ingress.kubernetes.io/config-backend: |
        option httpchk GET /ha/health HTTP/1.0
```

:::

Following changes are in case of usage haproxy ingress:

| File name                                       | Yaml path                                            | Value to set                               |
|:------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------|
| digitalai-release/kubernetes/dairelease_cr.yaml | spec.ingress.annotations.kubernetes.io/ingress.class | haproxy-custom-namespace-1-dai-xlr         |
| digitalai-release/kubernetes/dairelease_cr.yaml | spec.haproxy-ingress.fullnameOverride                | custom-namespace-1-dai-xlr-haproxy-ingress |
| digitalai-release/kubernetes/dairelease_cr.yaml | spec.haproxy-ingress.controller.ingressClass         | haproxy-custom-namespace-1-dai-xlr         |



### 7. Deploy to the cluster custom namespace

1. Do the step 3 from the documentation [Step 3—Update the Azure AKS Cluster Information](https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-3update-the-azure-aks-cluster-information)
2. Do the step 5 from the documentation [Step 5—Download and set up the XL CLI](https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-6set-up-the-xl-deploy-container-instance)
3. Do the step 6 from the documentation [Step 6—Set up the XL Deploy Container instance](https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-6set-up-the-xl-deploy-container-instance-1)
4. Do the step 7 from the documentation [Step 7—Activate the deployment process](https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-7activate-the-deployment-process-1)
5. Do the step 8 from the documentation [Step 8—Verify the deployment status](https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-8verify-the-deployment-status-1)

### 8. Apply any custom changes

If you have any custom changes that you collected previously in the step 3.3, you can apply them again in this step in the same way as before on the `default` namespace.

### 9. Wrap-up

Wait for all pods to ready and without any errors. 

If you used same host in the new custom namespace to the one that is on the `default` namespace, in that case XLR page is still opening from the `default` 
namespace. You need in that case apply step 9.a, after that on the configurated host will be available XLR that is from the new custom namespace.

In case of haproxy and one release pod, list of pods should look like following table:
```
│ NAMESPACE↑           NAME                                                          READY     RESTARTS STATUS  │
│ custom-namespace-1   custom-namespace-1-dai-xlr-haproxy-ingress-7df948c7d7-7xcrt   1/1              0 Running │
│ custom-namespace-1   dai-xlr-digitalai-release-0                                   1/1              0 Running │
│ custom-namespace-1   dai-xlr-postgresql-0                                          1/1              0 Running │
│ custom-namespace-1   dai-xlr-rabbitmq-0                                            1/1              0 Running │
│ custom-namespace-1   xlr-operator-controller-manager-78ff46dbb8-rq45l              2/2              0 Running │    
```

#### 9.a Destroy XLR in default namespace

If you are sure that everything is up and running on the new custom namespace, you can destroy previous setup on the `default` namespace, 
here are steps how to that:

```shell
# get the CR on default namespace and delete it
❯ kubectl get digitalaireleases.xlr.digital.ai dai-xlr -n default -o yaml > dai-xlr-default.yaml
❯ kubectl delete -n default -f dai-xlr-default.yaml

# get the deployment on default namespace and delete it
❯ kubectl get deployment -n default
❯ kubectl delete -n default deployment xlr-operator-controller-manager

# get the service on default namespace and delete it
❯ kubectl get service -n default
❯ kubectl delete -n default service xlr-operator-controller-manager-metrics-service

# get the role on default namespace and delete it
❯ kubectl get roles -n default
❯ kubectl delete -n default roles xlr-operator-leader-election-role

# get the roleBinding on default namespace and delete it
❯ kubectl get roleBinding -n default
❯ kubectl delete -n default roleBinding xlr-operator-leader-election-rolebinding

# get clusterRoles related to XLR on default namespace and delete them
❯ kubectl get clusterRoles
❯ kubectl delete clusterRoles xlr-operator-manager-role xlr-operator-metrics-reader xlr-operator-proxy-role

# get clusterRoleBinding related to XLR on default namespace and delete them
❯ kubectl get clusterRoleBinding
❯ kubectl delete clusterRoleBinding xlr-operator-proxy-rolebinding xlr-operator-manager-rolebinding

# get pvcs related to XLR on default namespace and delete them (list of the pvcs depends on what is enabled in the deployment)
❯ kubectl get pvc -n default
❯ kubectl delete -n default pvc data-dai-xlr-postgresql-0 data-dai-xlr-rabbitmq-0
```

You can also clean up any configmaps or secrets that are in the `default` namespace and related to the XLR.
