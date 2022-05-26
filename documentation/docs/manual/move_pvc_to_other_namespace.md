---
sidebar_position: 14
---

# C. How to change namespace of the PVC

## Prerequisites
- The kubectl command-line tool
- Access to a Kubernetes cluster with installed Release in the `default` namespace

Tested with:
- xl-release 10.3.9, 22.1.1
- xl-cli 22.1.1
- Azure cluster


## C.1. Backup everything

:::caution
Before doing any of the following steps backup everything:
- database data
- any custom configuration that was done for the operator setup
  - StatefulSets
  - Deployments
  - ConfigMaps
  - Secrets
  - CustomResource
  - anything else that was customized
- any volume related to release in the default namespace, for example data from the mounted volumes on the release pod:
  - /opt/xebialabs/xl-release-server/reports
  - /opt/xebialabs/xl-release-server/ext
  - /opt/xebialabs/xl-release-server/conf
:::


## C.2. Be sure to not delete PVs with your actions

Patch the all PVs to set the “persistentVolumeReclaimPolicy” to “Retain”, for example (if cluster admin's didn't do that already):

```
❯ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                 STORAGECLASS                                   REASON   AGE
pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            Delete           Bound    default/dai-xlr-digitalai-release   vp-azure-aks-test-cluster-file-storage-class            6h36m
...

❯ kubectl patch pv pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
persistentvolume/pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf patched
```

Export the current PVCs objects because it will be necessary to recreate the PVCs in a later stage:
```
❯ kubectl get pvc dai-xlr-digitalai-release -n default -o yaml > pvc-dai-xlr-digitalai-release.yaml
```

Iterate on all PVs that are connected to the XLR PVCs in the default namespace, list depends on the installed components. 
For example, here is list of PVCs that are usually in the default namespace:
- dai-xlr-digitalai-release
- data-dai-xlr-postgresql-0
- data-dai-xlr-rabbitmq-0

On the end check if all PVs have correct Reclaim Policy:

```
❯ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                      STORAGECLASS                                   REASON   AGE
pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            Retain           Bound    default/ai-xlr-digitalai-release           vp-azure-aks-test-cluster-file-storage-class            7h
...
```


## C.3. Stop everything that is using XLR PVC-s (and other PVC if needed)

:::caution
Be sure that you did backup of the CR before this step!
:::

If you are sure that everything is backuped and ready for installation on the new custom namespace, you can destroy previous setup on the `default` namespace,
here are steps how to do that:

```shell
# get the CR on default namespace and delete it
❯ kubectl get digitalaireleases.xlr.digital.ai dai-xlr -n default -o yaml > cr-dai-xlr-default.yaml
❯ kubectl delete -n default -f cr-dai-xlr-default.yaml

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
```

Do not delete PVs or PVCs we can reuse them on the new namespace.


## C.4. Move existing PVC to the custom namespace

Select one option that the best suites for your case.

Iterate one of the options on all PVs and PVCs that are connected to the XLR PVCs in the default namespace, list depends on the installed components.
For example, here is list of PVCs that are usually in the default namespace:
- dai-xlr-digitalai-release
- data-dai-xlr-postgresql-0
- data-dai-xlr-rabbitmq-0

### C.4.OPTION_1 Create PVC in the custom namespace by copying PV data

Make the copy of the `pvc-dai-xlr-digitalai-release.yaml` for the later reference. 
Edit file `pvc-dai-xlr-digitalai-release.yaml`:
1. Delete all the lines under sections:
- `status`
- `spec.volumneMode`
- `spec.volumneName`
- `metadata.uid`
- `metadata.resourceVersion`
- `metadata.ownerReferences`
- `metadata.namespace`
- `metadata.creationTimestamp`
- `metadata.finalizers`
- `metadata.annotations.pv.kubernetes.io/bind-completed`
- `metadata.annotations.pv.kubernetes.io/bound-by-controller`
2. Rename following lines by adding namespace name:
- `metadata.name` from dai-xlr-digitalai-release to dai-xlr-custom-namespace-1-digitalai-release
- `metadata.labels.release` from dai-xlr to dai-xlr-custom-namespace-1
- `metadata.annotations.meta.helm.sh/release-namespace` from default to custom-namespace-1
- `metadata.annotations.meta.helm.sh/release-name` from dai-xlr to dai-xlr-custom-namespace-1
  The renaming rule is to replace any occurrence of `dai-xlr` with `dai-xlr-{{custom_namespace_name}}`

Create those PVCs, but inside the Namespace “custom-namespace-1”:
```shell
❯ kubectl apply -f pvc-dai-xlr-digitalai-release.yaml -n custom-namespace-1
persistentvolumeclaim/dai-xlr-digitalai-release created
```
3. Check if PVC is bound
   Check the PVCs state, which will probably in Pending state, and after some time in Bound state:
```shell
❯ kubectl get pvc -n custom-namespace-1
NAME                                           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                                   AGE
dai-xlr-custom-namespace-1-digitalai-release   Bound    pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            vp-azure-aks-test-cluster-file-storage-class   3m33s
```

Start following pod:
1. Put following in file `pod-dai-pv-access-custom-namespace-1.yaml` (don't forget to update custom-namespace-1 with real namespace name):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dai-pv-access-custom-namespace-1
spec:
  containers:
    - name: sleeper
      command: ["sleep", "1d"]
      image: xebialabs/tiny-tools:22.2.0
      imagePullPolicy: Always
      volumeMounts:
        - mountPath: /opt/xebialabs/xl-release-server/reports
          name: reports-dir
          subPath: reports
        - mountPath: /opt/xebialabs/xl-release-server/work
          name: reports-dir
          subPath: work
        - mountPath: /opt/xebialabs/xl-release-server/conf
          name: reports-dir
          subPath: conf
        - mountPath: /opt/xebialabs/xl-release-server/ext
          name: reports-dir
          subPath: ext
        - mountPath: /opt/xebialabs/xl-release-server/hotfix
          name: reports-dir
          subPath: hotfix
        - mountPath: /opt/xebialabs/xl-release-server/hotfix/lib
          name: reports-dir
          subPath: lib
        - mountPath: /opt/xebialabs/xl-release-server/hotfix/plugins
          name: reports-dir
          subPath: plugins
        - mountPath: /opt/xebialabs/xl-release-server/log
          name: reports-dir
          subPath: log
  restartPolicy: Never
  volumes:
    - name: reports-dir
      persistentVolumeClaim:
        claimName: dai-xlr-custom-namespace-1-digitalai-release
```
Update the claimName with correct name!

2. Start the pod
```shell
❯ kubectl apply -f pod-dai-pv-access-custom-namespace-1.yaml -n custom-namespace-1
```

3. Put following in file `pod-dai-pv-access.yaml` for the default namespace:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dai-pv-access
spec:
  containers:
    - name: sleeper
      command: ["sleep", "1d"]
      image: xebialabs/tiny-tools:22.2.0
      imagePullPolicy: Always
      volumeMounts:
        - mountPath: /opt/xebialabs/xl-release-server/reports
          name: reports-dir
          subPath: reports
        - mountPath: /opt/xebialabs/xl-release-server/work
          name: reports-dir
          subPath: work
        - mountPath: /opt/xebialabs/xl-release-server/conf
          name: reports-dir
          subPath: conf
        - mountPath: /opt/xebialabs/xl-release-server/ext
          name: reports-dir
          subPath: ext
        - mountPath: /opt/xebialabs/xl-release-server/hotfix
          name: reports-dir
          subPath: hotfix
        - mountPath: /opt/xebialabs/xl-release-server/hotfix/lib
          name: reports-dir
          subPath: lib
        - mountPath: /opt/xebialabs/xl-release-server/hotfix/plugins
          name: reports-dir
          subPath: plugins
        - mountPath: /opt/xebialabs/xl-release-server/log
          name: reports-dir
          subPath: log
  restartPolicy: Never
  volumes:
    - name: reports-dir
      persistentVolumeClaim:
        claimName: dai-xlr-digitalai-release
```

4. Start the pod
```shell
❯ kubectl apply -f pod-dai-pv-access.yaml -n default
```

5. Copy data from one pod to 
```shell
kubectl exec -n default dai-pv-access -- tar cf - \
    /opt/xebialabs/xl-release-server/ext \
    /opt/xebialabs/xl-release-server/reports \
    | kubectl exec -n custom-namespace-1 -i dai-pv-access-custom-namespace-1 -- tar xvf - -C /
```

6. Chmod of the moved folder
```shell
kubectl exec -n custom-namespace-1 -i dai-pv-access-custom-namespace-1 -- chmod -R 777 /opt/xebialabs/xl-release-server/reports/
kubectl exec -n custom-namespace-1 -i dai-pv-access-custom-namespace-1 -- chmod -R 777 /opt/xebialabs/xl-release-server/ext/
```

7. Delete the pods
```shell
❯ kubectl delete pod dai-pv-access-custom-namespace-1 -n custom-namespace-1
❯ kubectl delete pod dai-pv-access -n default
```


### C.4.OPTION_2 Move existing PVC to the custom namespace by reusing PV

Following option will reuse PV in the new namespace, rollback of the option is more complicated. 

Delete the current PVC in the namespace `default` if it still exists (on older version from 22.2 dai-xlr-digitalai-release PVC will not exist):
```
❯ kubectl delete pvc dai-xlr-digitalai-release -n default
```

See that the related PV Status will be changed from `Bound` to `Released`:
```
❯ kubectl get pv pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM                                 STORAGECLASS                                   REASON   AGE
pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            Retain           Released   digitalai/dai-xlr-digitalai-release   vp-azure-aks-test-cluster-file-storage-class            7h36m
```

Edit each one of the PVs to remove the old references with claim:
```
❯ kubectl edit pv pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf
```
Remove lines like following example:
```yaml
...
claimRef:
    apiVersion: v1
    kind: PersistentVolumeClaim
    name: dai-xlr-digitalai-release
    namespace: default
    resourceVersion: "23284462"
    uid: 53564205-6e1e-45f0-9dcf-e21adefa6eaf
...
```

Check that there are no references anymore in the CLAIM column:
```
❯ kubectl get pv pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS                                   REASON   AGE
pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            Retain           Available           vp-azure-aks-test-cluster-file-storage-class            8h
```

Make the copy of the `pvc-dai-xlr-digitalai-release.yaml` for the later reference.
Edit file `pvc-dai-xlr-digitalai-release.yaml`:
1. Delete all the lines under section:
- `status`
- `metadata.namespace`
- `metadata.uid`
- `metadata.resourceVersion`
- `metadata.creationTimestamp`
- `metadata.finalizers`
- `metadata.annotations.pv.kubernetes.io/bind-completed`
- `metadata.annotations.pv.kubernetes.io/bound-by-controller`
- `metadata.ownerReferences`
2. Rename following lines by adding namespace name:
- `metadata.name` from dai-xlr-digitalai-release to dai-xlr-custom-namespace-1-digitalai-release
- `metadata.labels.release` from dai-xlr to dai-xlr-custom-namespace-1
- `metadata.annotations.meta.helm.sh/release-namespace` from default to custom-namespace-1
- `metadata.annotations.meta.helm.sh/release-name` from dai-xlr to dai-xlr-custom-namespace-1
  The renaming rule is to replace any occurrence of `dai-xlr` with `dai-xlr-{{custom_namespace_name}}`

Create those PVCs again, but inside the Namespace “custom-namespace-1”:
```
❯ kubectl apply -f pvc-dai-xlr-digitalai-release.yaml -n custom-namespace-1
persistentvolumeclaim/dai-xlr-custom-namespace-1-digitalai-release created
```

Check the PVCs state, which will probably in Pending state, and after some time in Bound state:
```
❯ kubectl get pvc -n custom-namespace-1
NAME                                           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                                   AGE
dai-xlr-custom-namespace-1-digitalai-release   Bound    pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            vp-azure-aks-test-cluster-file-storage-class   3m33s
```

On the moved PV for the release you will need to empty some folders, do that with following pod:
1. Put following in file `pod-dai-pv-access-custom-namespace-1.yaml` (don't forget to update custom-namespace-1 with real namespace name):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dai-pv-access-custom-namespace-1
spec:
  containers:
    - name: sleeper
      command: ["sleep", "1d"]
      image: xebialabs/tiny-tools:22.2.0
      imagePullPolicy: Always
      volumeMounts:
        - mountPath: /opt/xebialabs/xl-release-server/reports
          name: reports-dir
          subPath: reports
        - mountPath: /opt/xebialabs/xl-release-server/work
          name: reports-dir
          subPath: work
        - mountPath: /opt/xebialabs/xl-release-server/conf
          name: reports-dir
          subPath: conf
        - mountPath: /opt/xebialabs/xl-release-server/ext
          name: reports-dir
          subPath: ext
        - mountPath: /opt/xebialabs/xl-release-server/hotfix
          name: reports-dir
          subPath: hotfix
        - mountPath: /opt/xebialabs/xl-release-server/hotfix/lib
          name: reports-dir
          subPath: lib
        - mountPath: /opt/xebialabs/xl-release-server/hotfix/plugins
          name: reports-dir
          subPath: plugins
        - mountPath: /opt/xebialabs/xl-release-server/log
          name: reports-dir
          subPath: log
  restartPolicy: Never
  volumes:
    - name: reports-dir
      persistentVolumeClaim:
        claimName: dai-xlr-custom-namespace-1-digitalai-release
```
2. Start the pod
```shell
❯ kubectl apply -f pod-dai-pv-access-custom-namespace-1.yaml -n custom-namespace-1
```
3. Empty following folders from the pod:
- /opt/xebialabs/xl-release-server/work
- /opt/xebialabs/xl-release-server/conf
- /opt/xebialabs/xl-release-server/hotfix
- /opt/xebialabs/xl-release-server/hotfix/lib
- /opt/xebialabs/xl-release-server/hotfix/plugins

Example for the work folder:
```shell
❯ kubectl exec -n custom-namespace-1 -i dai-xlr-custom-namespace-1-digitalai-release-0  -- sh -c "rm -fr /opt/xebialabs/xl-release-server/conf/*"
```

4. Delete the pod
```shell
❯ kubectl delete pod dai-pv-access-custom-namespace-1 -n custom-namespace-1
```

Iterate on other PVs (for example you can migrate on the same way DB data if you are not using external Postgres, or if you are doing some other way of DB data migration).


### C.4.OPTION_3 Clone existing PVC to the custom namespace by CSI Volume Cloning

Please check following document if this option is possible for your Persisted Volume setup (there are some limitations when it is possible):

[CSI Volume Cloning](https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/)
