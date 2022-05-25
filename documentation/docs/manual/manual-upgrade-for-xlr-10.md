---
sidebar_position: 15
---

#  Manual helm to operator upgrade of xlr from version 10 to above 22.1 version. 

## Prerequisites
- The kubectl command-line tool
- Access to a Kubernetes cluster with installed Release in the `default` namespace

## 1. [Backup everything](https://xebialabs.github.io/xl-release-kubernetes-operator/docs/manual/move_pvc_to_other_namespace#c1-backup-everything)
## 2. [Update PV  RECLAIM POLICY To Retain](https://xebialabs.github.io/xl-release-kubernetes-operator/docs/manual/move_pvc_to_other_namespace/#c2-be-sure-to-not-delete-pvs-with-your-actions)

```shell
eg:
> kubectl patch pv pvc-1bc9fb12-b55b-4efa-a3b6-c25700b07c0e -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}';

[sishwarya@localhost xl-release-kubernetes-helm-chart] (10.0) $ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                STORAGECLASS          REASON   AGE
pvc-38314489-068a-42e7-bc65-cc9491c5457c   50Gi       RWO            Retain           Bound    default/data-xlr-prod-postgresql-0   aws-efs-provisioner            4m58s
pvc-6d03813b-1438-41ee-93c9-3f32efe73e47   8Gi        RWO            Retain           Bound    default/data-xlr-prod-rabbitmq-1     aws-efs-provisioner            4m13s
pvc-783d538b-532f-4ed5-a0be-2ce4fe91975e   5Gi        RWO            Retain           Bound    default/xlr-prod-digitalai-release   aws-efs-provisioner            5m
pvc-808b52b0-4851-44ff-a950-a61e4ff842ca   8Gi        RWO            Retain           Bound    default/data-xlr-prod-rabbitmq-2     aws-efs-provisioner            3m12s
pvc-f36a89a9-d48d-49dc-a210-a43c7d1a3862   8Gi        RWO            Retain           Bound    default/data-xlr-prod-rabbitmq-0     aws-efs-provisioner            4m58s

```    
## 3. Creating new PVC for dai-release by copying PV data.
:::note
eg: helm release name : xlr-prod
:::
### i. Make the copy of the pvc-xlr-prod-digitalai-release.yaml for the later reference.
   ```shell
   > kubectl get pvc xlr-prod-digitalai-release -o yaml > pvc-xlr-prod-digitalai-release.yaml.
   ```

### ii. Manually create pvc dai-xlr-digitalai-release as mentioned below.
  * Copy the pvc-release-name-digitalai-release.yaml file  to pvc-dai-xlr-digitalai-release.yaml
    ```shell
     > cp pvc-xlr-prod-digitalai-release.yaml pvc-dai-xlr-digitalai-release.yaml
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

### iii.  Create PVC dai-xlr-digitalai-release.
```shell
   > kubectl apply -f pvc-dai-xlr-digitalai-release.yaml
```
```shell
      [sishwarya@localhost docs] $ kubectl apply -f pvc-dai-xlr-digitalai-release.yaml
      persistentvolumeclaim/dai-xlr-digitalai-release created
```

### iv. Verify if PV bounded
  ```shell
  [sishwarya@localhost docs] $ kubectl get pvc dai-xlr-digitalai-release
  NAME                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
  dai-xlr-digitalai-release   Bound    pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2   5Gi        RWO            aws-efs-provisioner   53s
  
  [sishwarya@localhost docs] $ kubectl get pv pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2
  NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                               STORAGECLASS          REASON   AGE
  pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2   5Gi        RWO            Delete           Bound    default/dai-xlr-digitalai-release   aws-efs-provisioner            64s
  ```
  
### v. Update the Reclaim policy to Retain, for newly created pv of dai-xlr-digitalai-release.
  ```shell
   [sishwarya@localhost docs] $ kubectl patch pv pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2 -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}';
   persistentvolume/pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2 patched
   [sishwarya@localhost docs] $ kubectl get pv pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2
   NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                               STORAGECLASS          REASON   AGE
   pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2   5Gi        RWO            Retain           Bound    default/dai-xlr-digitalai-release   aws-efs-provisioner            3m40s
  ```

### vi. Start the following pod for accessing the newly created PVC [dai-xlr-digitalai-release].
  
  * Update the pod [pod-dai-xlr-digitalai-release.yaml] yaml with exact volumes which we mounted in previous installation.
  
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
    [sishwarya@localhost docs] $ kubectl apply -f pod-dai-xlr-digitalai-release.yaml
    pod/pod-dai-xlr-digitalai-release created
  ```
  ```shell
    [sishwarya@localhost docs] $ kubectl get pod/pod-dai-xlr-digitalai-release
    NAME                            READY   STATUS    RESTARTS   AGE
    pod-dai-xlr-digitalai-release   1/1     Running   0          34s
  ```
    * Verify the mouted path is available in newly created PV.
  ```shell
     [sishwarya@localhost docs] $ kubectl exec -it pod/pod-dai-xlr-digitalai-release -- sh
     / # cd /opt/xebialabs/xl-release-server/
     /opt/xebialabs/xl-release-server # ls -lrt reports
     total 0
     /opt/xebialabs/xl-release-server #
  ```

### vii. Copy data and Give Persmission.
 * Copy data from xlr-prod-digitalai-release-0 to pod-dai-xlr-digitalai-release

```shell
    > kubectl exec -n default xlr-prod-digitalai-release-0 -- tar cf - /opt/xebialabs/xl-release-server/reports | kubectl exec -n default -i pod-dai-xlr-digitalai-release -- tar xvf - -C /
  ```
```shell
eg:
    [sishwarya@localhost docs] $ kubectl exec -n default xlr-prod-digitalai-release-0 -- tar cf - /opt/xebialabs/xl-release-server/reports | kubectl exec -n default -i pod-dai-xlr-digitalai-release -- tar xvf - -C /
    Defaulted container "digitalai-release" out of: digitalai-release, wait-for-db (init)
    tar: Removing leading `/' from member names
    opt/xebialabs/xl-release-server/reports/
    opt/xebialabs/xl-release-server/reports/testupgrade/
    opt/xebialabs/xl-release-server/reports/testupgrade/readme.txt
    opt/xebialabs/xl-release-server/reports/readme.txt
```
 * Give full Permission to the copied data in new PV.
  ```shell
    [sishwarya@localhost docs] $ kubectl exec -it pod/pod-dai-xlr-digitalai-release -- sh
    / # cd /opt/xebialabs/xl-release-server/
    /opt/xebialabs/xl-release-server # chmod -R 777 reports/
    /opt/xebialabs/xl-release-server # ls -lrt  reports
    total 8
    -rwxrwxrwx 1 10001 40071 2036 May 25 03:50 readme.txt
    drwxrwsrwx 2 10001 40071 6144 May 25 03:54 testupgrade
  ```
### viii.  Delete the pod.
```shell
      [sishwarya@localhost docs] $ kubectl delete pod/pod-dai-xlr-digitalai-release
       pod "pod-dai-xlr-digitalai-release" deleted
```

## 4. Run upgrade with dry run, with custom zip options.
  ```shell
     xl op --upgrade --dry-run
  ```

## 5. Take backup of existing password.
  ```shell
   ## To get the admin password for xl-release, run:
   kubectl get secret --namespace default xlr-prod-digitalai-release -o jsonpath="{.data.release-password}" | base64 --decode; echo
   
   ## To get the password for postgresql, run:
   kubectl get secret --namespace default xlr-prod-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode; echo
   
   ## To get the password for rabbitMQ, run:
   kubectl get secret --namespace default xlr-prod-rabbitmq  -o jsonpath="{.data.rabbitmq-password}" | base64 --decode; echo
  ```

## 6. Do following changes in the xebialabs/dai-release/dairelease_cr.yaml, based on the requirement.
### i. To update admin password 
 * Default  release admin password is "admin", if we need to update below fields.
```shell
    .spec.AdminPassword: <password from previous installation>
```
### ii.  To setup haproxy/nginx.
  * haproxy setup   
    ```shell
       .spec.haproxy-ingress.install = true
       .spec.nginx-ingress-controller.install = false
       .spec.ingress.path = "/"
               
       ## in the spec.ingress.annotations replace all nginx. settings and put:
       kubernetes.io/ingress.class: "haproxy"
       ingress.kubernetes.io/ssl-redirect: "false"
       ingress.kubernetes.io/rewrite-target: /
       ingress.kubernetes.io/affinity: cookie
       ingress.kubernetes.io/session-cookie-name: JSESSIONID
       ingress.kubernetes.io/session-cookie-strategy: prefix
       ingress.kubernetes.io/config-backend: |
       option httpchk GET /ha/health HTTP/1.0
    ```
  * nginx controller
    ```shell
       .spec.haproxy-ingress.install = false
       .spec.nginx-ingress-controller.install = true
    ```

### iii. To reuse existing claim for postgres/rabbitmq 
* If the release name is different from "dai-xlr" and if we are using embedded database, we need to reuse the existing Claim, for data persistence.
  
  * Update the following field with existing claim.
    
  ```shell
            .spec.postgresql.persistence.existingClaim
            .spec.rabbitmq.persistence.existingClaim --> not required, as we dont save any data.
  ```  
  ```shell
  eg:
      .spec.postgresql.persistence.existingClaim: data-xlr-prod-postgresql-0
  ```
   
  :::note
   If we are having more than one existing PVC for rabbitmq, we don't use  existingClaim for rabbitmq configuration, instead we can follow the other approach mentioned below for PV reuse.
  :::
       
  * Post helm uninstall, we can also edit postgres/rabbitmq PV as follows, to create the new PVC with existing PV.
    * Update the postgres pv with following details.      
      ```shell
                  claimRef:
                    apiVersion: v1
                    kind: PersistentVolumeClaim
                    name: data-dai-xlr-postgresql-0
                    namespace: default   
      ```
    * Update the rabbitmq pv with following details if we need to reuse the PV of rabbitmq.
     ```shell
                 claimRef:
                   apiVersion: v1
                   kind: PersistentVolumeClaim
                   name: data-dai-xlr-rabbitmq-0
                   namespace: default   
     ```   
    * Remove the following from PV [postgres/rabbitmq] while editing.
      ```shell
                 claimRef:
                  uid:
                  resourceVersion:
      ```
### iv. To setup oidc 
 * By default keycloak will be enabled as default oidc provider.
      * To disable oidc and keycloak.
           ```shell
              .spec.keycloak.install = false
              .spec.oidc.enabled =  false
           ```
      * To disable keycloak and enable external oidc.
           ```shell
              .spec.keycloak.install = false
              .spec.oidc.enabled =  true
              .spec.oidc.external = true
              ##  update the below fields with external oidc configuration
              .spec.oidc.accessTokenUri:
              .spec.oidc.clientId:
              .spec.oidc.clientSecret:
              .spec.oidc.emailClaim:
              .spec.oidc.external:
              .spec.oidc.fullNameClaim:
              .spec.oidc.issuer:
              .spec.oidc.keyRetrievalUri:
              .spec.oidc.logoutUri:
              .spec.oidc.postLogoutRedirectUri:
              .spec.oidc.redirectUri:
              .spec.oidc.rolesClaim:
              .spec.oidc.userAuthorizationUri:
              .spec.oidc..userNameClaim:
           ```
      * If keycloak is enabled, then we will be using default embedded database.
        :::caution
                Note:
                    * Post upgrade keycloak pod failed to start with below error. 
                        Caused by: org.postgresql.util.PSQLException: FATAL: password authentication failed for user "keycloak"
                    * We need to Connect to the pod/dai-xlr-postgresql-0 pod and create the keycloak database.
                        * kuebctl exec -it pod/dai-xlr-postgresql-0 -- bash
                        * psql -U postgres
                        * create database keycloak;
                        * create user keycloak with encrypted password 'keycloak';
                        * grant all privileges on database keycloak to keycloak;
        
        :::
        :::note
        [Postgres password from previous installation](http://localhost:3000/xl-release-kubernetes-operator/docs/manual/manual-upgrade-for-xlr-10#5-take-backup-of-existing-password).
        :::

## 7. Bring up the xl-deploy in docker.

```shell
 docker run -e "ADMIN_PASSWORD=desired-admin-password" -e "ACCEPT_EULA=Y" -p 4516:4516 --name xld xebialabs/xl-deploy:22.1
```

## 8. Run the following command.
```shell
xl apply -f xebialabs/xebialabs.yaml
```

## 9. Verify the PVC and PV.
```shell
[sishwarya@localhost xl-release-kubernetes-operator] (D-21331) $ kubectl get pvc
NAME                         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
dai-xlr-digitalai-release    Bound    pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2   5Gi        RWO            aws-efs-provisioner   146m
data-dai-xlr-rabbitmq-0      Bound    pvc-51e2a5f0-8313-4930-a7b7-b7f648064a0a   8Gi        RWO            aws-efs-provisioner   5m32s
data-dai-xlr-rabbitmq-1      Bound    pvc-3eb28b33-e45f-4064-a762-fea483d21552   8Gi        RWO            aws-efs-provisioner   5m32s
data-dai-xlr-rabbitmq-2      Bound    pvc-8d171e3a-5b3e-4fb3-8873-00db6ada9a4b   8Gi        RWO            aws-efs-provisioner   5m32s
data-xlr-prod-postgresql-0   Bound    pvc-38314489-068a-42e7-bc65-cc9491c5457c   50Gi       RWO            aws-efs-provisioner   158m
data-xlr-prod-rabbitmq-0     Bound    pvc-f36a89a9-d48d-49dc-a210-a43c7d1a3862   8Gi        RWO            aws-efs-provisioner   158m
data-xlr-prod-rabbitmq-1     Bound    pvc-6d03813b-1438-41ee-93c9-3f32efe73e47   8Gi        RWO            aws-efs-provisioner   158m
data-xlr-prod-rabbitmq-2     Bound    pvc-808b52b0-4851-44ff-a950-a61e4ff842ca   8Gi        RWO            aws-efs-provisioner   157m

[sishwarya@localhost xl-release-kubernetes-operator] (D-21331) $ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM                                STORAGECLASS          REASON   AGE
pvc-38314489-068a-42e7-bc65-cc9491c5457c   50Gi       RWO            Retain           Bound      default/data-xlr-prod-postgresql-0   aws-efs-provisioner            159m
pvc-3eb28b33-e45f-4064-a762-fea483d21552   8Gi        RWO            Delete           Bound      default/data-dai-xlr-rabbitmq-1      aws-efs-provisioner            5m41s
pvc-51e2a5f0-8313-4930-a7b7-b7f648064a0a   8Gi        RWO            Delete           Bound      default/data-dai-xlr-rabbitmq-0      aws-efs-provisioner            5m41s
pvc-6d03813b-1438-41ee-93c9-3f32efe73e47   8Gi        RWO            Retain           Bound      default/data-xlr-prod-rabbitmq-1     aws-efs-provisioner            158m
pvc-783d538b-532f-4ed5-a0be-2ce4fe91975e   5Gi        RWO            Retain           Released   default/xlr-prod-digitalai-release   aws-efs-provisioner            159m
pvc-808b52b0-4851-44ff-a950-a61e4ff842ca   8Gi        RWO            Retain           Bound      default/data-xlr-prod-rabbitmq-2     aws-efs-provisioner            157m
pvc-8d171e3a-5b3e-4fb3-8873-00db6ada9a4b   8Gi        RWO            Delete           Bound      default/data-dai-xlr-rabbitmq-2      aws-efs-provisioner            5m41s
pvc-dad9e7c3-ae1b-4b28-b595-4f4b281a0bf2   5Gi        RWO            Retain           Bound      default/dai-xlr-digitalai-release    aws-efs-provisioner            146m
pvc-f36a89a9-d48d-49dc-a210-a43c7d1a3862   8Gi        RWO            Retain           Bound      default/data-xlr-prod-rabbitmq-0     aws-efs-provisioner            159m

[sishwarya@localhost xl-release-kubernetes-operator] (D-21331) $ 

```
:::note
Note:
 * We will see new PVC and PV created for rabbitmq, we can delete the old PVC and PV.
    * kubectl delete pvc data-xlr-prod-rabbitmq-0 data-xlr-prod-rabbitmq-1 data-xlr-prod-rabbitmq-2
    * kubectl delete pv pvc-f36a89a9-d48d-49dc-a210-a43c7d1a3862, pvc-6d03813b-1438-41ee-93c9-3f32efe73e47, pvc-808b52b0-4851-44ff-a950-a61e4ff842ca
 * We are reusing the existing claim for postgres.
 * Newly created PVC dai-xlr-digitalai-release for xl-release pod.
:::
    
   