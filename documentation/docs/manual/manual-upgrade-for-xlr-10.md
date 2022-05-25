---
sidebar_position: 15
---

#  Manual helm to operator upgrade of xlr from version 10 to 22.1 or latest 

## Prerequisites
- The kubectl command-line tool
- Access to a Kubernetes cluster with installed Release in the `default` namespace

## 1. [Backup everything](https://xebialabs.github.io/xl-release-kubernetes-operator/docs/manual/move_pvc_to_other_namespace#c1-backup-everything)
## 2. [Update PV  RECLAIM POLICY To Retain](https://xebialabs.github.io/xl-release-kubernetes-operator/docs/manual/move_pvc_to_other_namespace/#c2-be-sure-to-not-delete-pvs-with-your-actions)
eg:
```shell
kubectl patch pv pvc-1bc9fb12-b55b-4efa-a3b6-c25700b07c0e -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}';

[sishwarya@localhost xl-release-kubernetes-helm-chart] (10.0) $ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                STORAGECLASS          REASON   AGE
pvc-38314489-068a-42e7-bc65-cc9491c5457c   50Gi       RWO            Retain           Bound    default/data-xlr-prod-postgresql-0   aws-efs-provisioner            4m58s
pvc-6d03813b-1438-41ee-93c9-3f32efe73e47   8Gi        RWO            Retain           Bound    default/data-xlr-prod-rabbitmq-1     aws-efs-provisioner            4m13s
pvc-783d538b-532f-4ed5-a0be-2ce4fe91975e   5Gi        RWO            Retain           Bound    default/xlr-prod-digitalai-release   aws-efs-provisioner            5m
pvc-808b52b0-4851-44ff-a950-a61e4ff842ca   8Gi        RWO            Retain           Bound    default/data-xlr-prod-rabbitmq-2     aws-efs-provisioner            3m12s
pvc-f36a89a9-d48d-49dc-a210-a43c7d1a3862   8Gi        RWO            Retain           Bound    default/data-xlr-prod-rabbitmq-0     aws-efs-provisioner            4m58s

```    
## 3. Creating new PVC for dai-release by copying PV data.

* Make the copy of the pvc-<release-name>-digitalai-release.yaml for the later reference.
   ```shell
   > kubectl get pvc <release-name>-digitalai-release -o yaml > pvc-<release-name>-digitalai-release.yaml.
   ```
  
* Manually create pvc dai-xlr-digitalai-release as mentioned below.
  * Copy the pvc-<release-name>-digitalai-release.yaml file  to pvc-dai-xlr-digitalai-release.yaml
    ```shell
     cp pvc-xlr-prod-digitalai-release.yaml pvc-dai-xlr-digitalai-release.yaml
    ```
  * Delete all the lines under sections:
     ```shell
    status
    spec.volumneMode
    spec.volumneName
    metadata.uid
    metadata.resourceVersion
    metadata.ownerReferences
    metadata.namespace
    metadata.creationTimestamp
    metadata.finalizers
    metadata.annotations.pv.kubernetes.io/bind-completed
    metadata.annotations.pv.kubernetes.io/bound-by-controller
    ```
  * Update the following in yaml:
    ```shell
    metadata.name from <release-name>-digitalai-release to dai-xlr-digitalai-release
    metadata.labels.release: dai-xlr
    metadata.annotations.meta.helm.sh/release-namespace: default
    metadata.annotations.meta.helm.sh/release-name : dai-xlr
    etadata.annotations:helm.sh/resource-policy: keep 
    ``` 

*  Create PVC dai-xlr-digitalai-release.
   ```shell
    kubectl apply -f pvc-dai-xlr-digitalai-release.yaml
    ```
   ```shell
    [sishwarya@localhost docs] $ kubectl apply -f pvc-dai-xlr-digitalai-release.yaml
    persistentvolumeclaim/dai-xlr-digitalai-release created
    ```
   
* Verify if PV bounded
  ```shell
  [sishwarya@localhost docs] $ kubectl get pvc dai-xlr-digitalai-release
  NAME                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
  dai-xlr-digitalai-release   Bound    pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2   5Gi        RWO            aws-efs-provisioner   53s
  
  [sishwarya@localhost docs] $ kubectl get pv pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2
  NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                               STORAGECLASS          REASON   AGE
  pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2   5Gi        RWO            Delete           Bound    default/dai-xlr-digitalai-release   aws-efs-provisioner            64s
  ```
  
* Update the Reclaim policy to Retain for newly created pv for pvc dai-xlr-digitalai-release.
  ```shell
   [sishwarya@localhost docs] $ kubectl patch pv pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2 -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}';
   persistentvolume/pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2 patched
   [sishwarya@localhost docs] $ kubectl get pv pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2
   NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                               STORAGECLASS          REASON   AGE
   pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2   5Gi        RWO            Retain           Bound    default/dai-xlr-digitalai-release   aws-efs-provisioner            3m40s
  ```

* Start the following pod for accessing the newly created PV [pod-dai-xlr-digitalai-release.yaml] and copy the data.
  
  * Update the pod yaml with exact volumes which we mounted in previous installation.
  
  ```shell
      apiVersion: v1
      kind: Pod
      metadata:
      name: pod-dai-xlr-digitalai-release
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
      restartPolicy: Never
      volumes:
      - name: reports-dir
      persistentVolumeClaim:
      claimName: dai-xlr-digitalai-release
  ```
  * Start the pod
  ```shell

  ```