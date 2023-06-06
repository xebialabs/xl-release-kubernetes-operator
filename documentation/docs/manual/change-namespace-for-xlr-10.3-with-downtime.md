---
sidebar_position: 13
---

# How to change namespace with downtime

:::caution
This is internal documentation. This document can be used only if it was recommended by the Support Team.
:::

:::caution
This setup is deprecated from the 22.3 version.
:::

# B. How to change namespace in case there is release already running in the default namespace - with downtime

## Prerequisites
- The kubectl command-line tool
- Access to a Kubernetes cluster with installed Release in the `default` namespace

Tested with:
- xl-deploy 22.1.2
- xl-release 10.3.5, 10.3.9 upgraded to 22.1.2
- xl-cli 22.1.2
- Azure cluster

If you have already setup of the XLR default namespace it is possible to move the deployment to the custom namespace. Here we will use for example 
`custom-namespace-1`.

In the example we will use XLR 10.3 that will be upgraded to 22.1.2 version with latest 22.1.x operator image xebialabsunsupported/release-operator:22.1.0-519.949 from the 
[https://hub.docker.com/r/xebialabsunsupported/release-operator/tags](https://hub.docker.com/r/xebialabsunsupported/release-operator/tags) and latest operator 
package from the 22.1.x branch.

## Steps to setup operator on the custom namespace

With following steps you will setup XLR in the custom namespace, by first stopping the setup in the `default` namespace and after starting it in the custom namespace.

:::caution
Before doing any of the following steps backup everything:
- database data
- any custom configuration that was done for the operator setup
- any volume related to release in the default namespace, for example data from the mounted volumes on the release pod:
  - /opt/xebialabs/xl-release-server/reports
  - /opt/xebialabs/xl-release-server/ext
  - /opt/xebialabs/xl-release-server/conf
:::

### B.1. Create custom namespace

Setup custom namespace on Kubernetes cluster, `custom-namespace-1` for example:
```
❯ kubectl create namespace custom-namespace-1
```

Replace `custom-namespace-1` name in this and following steps with your custom namespace name.

### B.2. Backup everything on cluster

1. Collect all custom changes that are done in the `default` namespace for XLR resources
    - StatefulSets
    - Deployments
    - ConfigMaps
    - Secrets
    - CustomResource
    - anything else that was customized
2. Collect any other change that was done during initial setup according to the 
[https://docs.xebialabs.com/v.22.1/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#installing-deploy-on-azure-kubernetes-service](https://docs.xebialabs.com/v.22.1/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#installing-deploy-on-azure-kubernetes-service)
3. If you are using your own database and messaging queue setup, do the data backup. 

:::note
Note:
Any data migration is out of scope of this document. For example in case of database data migration, check with your DB admins what to do in that case.
For the external database case the best option is to migrate database to a new database schema, and use that schema on the new namespace.
:::


### B.3. Prepare the release operator

1. Get the release operator package zip for Azure: release-operator-azure-aks-22.1.0-519.949.zip (correct operator image is already setup in the package).

2. Download and set up the XL CLI setup (xl cli version in this case 22.1.2) from https://dist.xebialabs.com/public/xl-cli/22.1.2/
   Do the step 6 from the documentation [Step 6—Download and set up the XL CLI](https://docs.xebialabs.com/v.22.1/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-6download-and-set-up-the-xl-cli)
```shell
❯ ./xl version
CLI version:             22.1.2
Git version:             v22.1.1-0-g3d9c31d
API version XL Deploy:   xl-deploy/v1
API version XL Release:  xl-release/v1
Git commit:              3d9c31d7985ba22624cc78d48172237875ee6cae
Build date:              2022-04-18T12:39:39.622Z
GO version:              go1.16
OS/Arch:                 darwin/amd64
```

3. Do the step 7 from the documentation [Step 7—Set up the XL Deploy Container instance](https://docs.xebialabs.com/v.22.1/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-7set-up-the-xl-deploy-container-instance-1)
Use the 22.1.2 version of the deploy: `docker run -d -e "ADMIN_PASSWORD=admin" -e "ACCEPT_EULA=Y" -p 4516:4516 --name xld xebialabs/xl-deploy:22.1.2`

4. Run the upgrade setup with a dry run and generate the blueprint file:

In the last question `Edit list of custom resource keys that will migrate to the new Release CR` append following keys to the of the file:
```
.spec.ingress.annotations
```

Here is sample of the responses:
```
❯ xl op --upgrade --dry-run
? Select the setup mode? advanced
? Select the Kubernetes setup where the digitalai Devops Platform will be installed or uninstalled: AzureAKS [Azure AKS]
? Do you want to use Kubernetes' current-context from ~/.kube/config? Yes
? Do you want to use an existing Kubernetes namespace? Yes
? Enter the name of the existing Kubernetes namespace where the XebiaLabs DevOps Platform will be installed, updated or undeployed: default
? Product server you want to perform upgrade for daiRelease [Digital.ai Release]
? Enter the repository name(eg: <repositoryName>/<imageName>:<tagName>) xebialabs
? Enter the image name(eg: <repositoryName>/<imageName>:<tagName>) xl-release
? Enter the image tag(eg: <repositoryName>/<imageName>:<tagName>) 22.1.2
? Choose the version of the XL Deploy for Upgrader setup of operator 22.1.2
? Use embedded keycloak? No
? Select the type of upgrade you want. operatorToOperator [Operator to Operator]
? Operator image to use xebialabsunsupported/release-operator:22.1.0-519.949
? Do you want to use custom operator zip file for Release? Yes
? Release operator zip to use (absolute path or URL to the zip) /absolute_path_to_provided_zip/release-operator-azure-aks-22.1.0-519.949.zip
? Enter the name of custom resource. dai-xlr
? Enter the name of custom resource definition. digitalaireleases.xlr.digital.ai
? Edit list of custom resource keys that will migrate to the new Release CR <Received>
```

That will create files and directories in the working directory. The main directory is `xebialabs` and inside it are all template files that we need to edit.
Check the `xebialabs/dai-release/dairelease_cr.yaml` if all values are correctly set there.

:::note
Note:
Ignore question `Choose the version of the XL Deploy for Upgrader setup of operator`, we are not starting XL Deploy with this step,
because we have it already running in the step B.3.3. 
:::

### B.4. Update the release operator package to support custom namespace (common part)

Update following files (relative to the provider's directory) with custom namespace name:

| File name                                                                   | Yaml path                                     | Value to set                                             |
|:----------------------------------------------------------------------------|:----------------------------------------------|:---------------------------------------------------------|
| xebialabs/xl-k8s-foundation.yaml [kind: Infrastructure]                     | spec[0].children[0].children[0].name          | custom-namespace-1                                       |
| xebialabs/xl-k8s-foundation.yaml [kind: Infrastructure]                     | spec[0].children[0].children[0].namespaceName | custom-namespace-1                                       |
| xebialabs/xl-k8s-foundation.yaml [kind: Environments]                       | spec[0].children[0].members[1]                | - Infrastructure/DIGITALAI/K8s-MASTER/custom-namespace-1 |
| xebialabs/dai-release/template-generic/cluster-role-digital-proxy-role.yaml | metadata.name                                 | custom-namespace-1-xlr-operator-proxy-role               |
| xebialabs/dai-release/template-generic/cluster-role-manager-role.yaml       | metadata.name                                 | custom-namespace-1-xlr-operator-manager-role             |
| xebialabs/dai-release/template-generic/cluster-role-metrics-reader.yaml     | metadata.name                                 | custom-namespace-1-xlr-operator-metrics-reader           |
| xebialabs/dai-release/template-generic/leader-election-rolebinding.yaml     | subjects[0].namespace                         | custom-namespace-1                                       |
| xebialabs/dai-release/template-generic/manager-rolebinding.yaml             | metadata.name                                 | custom-namespace-1-xlr-operator-manager-rolebinding      |
| xebialabs/dai-release/template-generic/manager-rolebinding.yaml             | roleRef.name                                  | custom-namespace-1-xlr-operator-manager-role             |
| xebialabs/dai-release/template-generic/manager-rolebinding.yaml             | subjects[0].namespace                         | custom-namespace-1                                       |
| xebialabs/dai-release/template-generic/proxy-rolebinding.yaml               | metadata.name                                 | custom-namespace-1-xlr-operator-proxy-rolebinding        |
| xebialabs/dai-release/template-generic/proxy-rolebinding.yaml               | roleRef.name                                  | custom-namespace-1-xlr-operator-proxy-role               |
| xebialabs/dai-release/template-generic/proxy-rolebinding.yaml               | subjects[0].namespace                         | custom-namespace-1                                       |
| xebialabs/dai-release/dairelease_cr.yaml                                    | metadata.name                                 | dai-xlr-custom-namespace-1                               |
| xebialabs/dai-release/dairelease_cr.yaml                                    | spec.keycloak.install                         | false                                                    |


In the `xebialabs/dai-release/template-generic/deployment.yaml` add `env` section after `spec.template.spec.containers[1].image` (in the same level):
```yaml
        image: xebialabs...
        env:
          - name: WATCH_NAMESPACE
            valueFrom:
              fieldRef:
                fieldPath: metadata.namespace
        livenessProbe: 
          ...
```

In the `xebialabs/dai-release-operator.yaml` delete array element from the `spec[0].children[0].deployables`, where name is `name: custom-resource-definition`.
This will not deploy again CRD, as it already exists, when it was deployed for the first time. Example of the element to delete
```yaml
      - name: custom-resource-definition
        type: k8s.ResourcesFile
        fileEncodings:
          ".+\\.properties": ISO-8859-1
        mergePatchType: strategic
        propagationPolicy: Foreground
        updateMethod: patch
        createOrder: "3"
        modifyOrder: "2"
        destroyOrder: "1"
        file: !file "dai-release/template-generic/custom-resource-definition.yaml"
```

### B.4.a. Update the release operator package to support custom namespace - only in case of Nginx ingress controller

Following changes are in case of usage nginx ingress (default behaviour):

| File name                                | Yaml path                                             | Value to set                     |
|:-----------------------------------------|:------------------------------------------------------|:---------------------------------|
| xebialabs/dai-release/dairelease_cr.yaml | spec.ingress.annotations.kubernetes.io/ingress.class  | nginx-dai-xlr-custom-namespace-1 |
| xebialabs/dai-release/dairelease_cr.yaml | spec.nginx-ingress-controller.extraArgs.ingress-class | nginx-dai-xlr-custom-namespace-1 |
| xebialabs/dai-release/dairelease_cr.yaml | spec.nginx-ingress-controller.ingressClass            | nginx-dai-xlr-custom-namespace-1 |


### B.4.b. Update the release operator package to support custom namespace - only in case of Haproxy ingress controller

:::note
Note:
To setup haproxy instead of default nginx configuration that is provided in the operator package you need to do following changes in the
`xebialabs/dai-release/dairelease_cr.yaml`:
- `spec.haproxy-ingress.install = true`
- `spec.nginx-ingress-controller.install = false`
- `spec.ingress.path = "/"`
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

| File name                                 | Yaml path                                            | Value to set                       |
|:------------------------------------------|:-----------------------------------------------------|:-----------------------------------|
| xebialabs/dai-release/dairelease_cr.yaml  | spec.ingress.annotations.kubernetes.io/ingress.class | haproxy-dai-xlr-custom-namespace-1 |
| xebialabs/dai-release/dairelease_cr.yaml  | spec.haproxy-ingress.controller.ingressClass         | haproxy-dai-xlr-custom-namespace-1 |


### B.5. Update additionally YAML files

Apply all collected changes from the `default` namespace to the CR in the release operator package `xebialabs/dai-release/dairelease_cr.yaml`.
(The best is to compare new CR `xebialabs/dai-release/dairelease_cr.yaml` with the one from the `default` namespace)

Check the YAML files, and update them with additional changes. For example CR YAML and update it with any missing custom configuration. 

If you are using your own database and messaging queue setup, setup it in the same way as in the `default` namespace,
 in the new CR in the release operator package `xebialabs/dai-release/dairelease_cr.yaml`. 
Database in this case of setup can be reused if there is network visibility in the new namespace where you are moving your installation


For example you can do now OIDC setup, add the following fields with value under spec tag, for enabling oidc in the `xebialabs/dai-release/dairelease_cr.yaml`
```
spec:
  oidc:
    enabled: true
    accessTokenUri: null
    clientId: null
    clientSecret: null
    emailClaim: null
    external: true
    fullNameClaim: null
    issuer: null
    keyRetrievalUri: null
    logoutUri: null
    postLogoutRedirectUri: null
    redirectUri: null
    rolesClaim: null
    userAuthorizationUri: null
    userNameClaim: null
    scopes: ["openid"]
```
Replace nulls with correct values, for more info check [documentation](https://docs.xebialabs.com/v.22.1/release/concept/xl-release-oidc-authentication/#client-authentication)

### B.6. Be sure to not delete PVs

Do the step from [C.2. Be sure to not delete PVs with you actions](move_pvc_to_other_namespace.md#c2-be-sure-to-not-delete-pvs-with-your-actions)

### B.7. Destroy XLR in default namespace

Do the step from [C.3. Stop everything that is using XLR PVC-s](move_pvc_to_other_namespace.md#c3-stop-everything-that-is-using-xlr-pvc-s-and-other-pvc-if-needed)

### B.8. Move existing PVCs to the custom namespace

There are 3 options from the step from [C.4. Move existing PVC to the custom namespace](move_pvc_to_other_namespace.md#c4-move-existing-pvc-to-the-custom-namespace)

### B.9. Deploy to the custom namespace

1. We are using here yaml that was result of the upgrade dry-run in the working directory, so we should apply against following file:
```
xl apply -f ./xebialabs.yaml
```

2. Do the step 9, 10 and 11 from the documentation [Step 9—Verify the deployment status](https://docs.xebialabs.com/v.22.1/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-10verify-if-the-deployment-was-successful-1)


### B.10. Apply any custom changes

If you have any custom changes that you collected previously in the step 3.3, you can apply them again in this step in the same way as before on the `default` namespace.

Check if PVCs and PVs are reused by the new setup in the custom namespace.

### B.11. Wrap-up

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
Table could have different entries if you nginx or using external postgresql and rabbitmq.

#### B.12 Destroy remains of XLR in default namespace

If you are sure that everything is up and running on the new custom namespace, you can destroy remaining setup in the `default` namespace:

```shell
# be careful if you would like really to delete all PVC-s and related PV-s, backup before delete
# get pvcs related to XLR on default namespace and delete them (list of the pvcs depends on what is enabled in the deployment)
❯ kubectl get pvc -n default
❯ kubectl delete -n default pvc data-dai-xlr-rabbitmq-0 ...
```

You can also clean up any configmaps or secrets that are in the `default` namespace and related to the XLR.

You also delete all PVs that were connected to the XLR installation in the default namespace, and are not migrated and used by the custom namespace.
