"use strict";(self.webpackChunkdocumentation=self.webpackChunkdocumentation||[]).push([[620],{3905:function(e,a,t){t.d(a,{Zo:function(){return m},kt:function(){return d}});var n=t(7294);function l(e,a,t){return a in e?Object.defineProperty(e,a,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[a]=t,e}function r(e,a){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);a&&(n=n.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),t.push.apply(t,n)}return t}function i(e){for(var a=1;a<arguments.length;a++){var t=null!=arguments[a]?arguments[a]:{};a%2?r(Object(t),!0).forEach((function(a){l(e,a,t[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):r(Object(t)).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(t,a))}))}return e}function o(e,a){if(null==e)return{};var t,n,l=function(e,a){if(null==e)return{};var t,n,l={},r=Object.keys(e);for(n=0;n<r.length;n++)t=r[n],a.indexOf(t)>=0||(l[t]=e[t]);return l}(e,a);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(n=0;n<r.length;n++)t=r[n],a.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(l[t]=e[t])}return l}var s=n.createContext({}),p=function(e){var a=n.useContext(s),t=a;return e&&(t="function"==typeof e?e(a):i(i({},a),e)),t},m=function(e){var a=p(e.components);return n.createElement(s.Provider,{value:a},e.children)},c={inlineCode:"code",wrapper:function(e){var a=e.children;return n.createElement(n.Fragment,{},a)}},u=n.forwardRef((function(e,a){var t=e.components,l=e.mdxType,r=e.originalType,s=e.parentName,m=o(e,["components","mdxType","originalType","parentName"]),u=p(t),d=l,k=u["".concat(s,".").concat(d)]||u[d]||c[d]||r;return t?n.createElement(k,i(i({ref:a},m),{},{components:t})):n.createElement(k,i({ref:a},m))}));function d(e,a){var t=arguments,l=a&&a.mdxType;if("string"==typeof e||l){var r=t.length,i=new Array(r);i[0]=u;var o={};for(var s in a)hasOwnProperty.call(a,s)&&(o[s]=a[s]);o.originalType=e,o.mdxType="string"==typeof e?e:l,i[1]=o;for(var p=2;p<r;p++)i[p]=t[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,t)}u.displayName="MDXCreateElement"},8607:function(e,a,t){t.r(a),t.d(a,{frontMatter:function(){return o},contentTitle:function(){return s},metadata:function(){return p},toc:function(){return m},default:function(){return u}});var n=t(7462),l=t(3366),r=(t(7294),t(3905)),i=["components"],o={sidebar_position:14},s="C. How to change namespace of the PVC",p={unversionedId:"manual/move_pvc_to_other_namespace",id:"manual/move_pvc_to_other_namespace",isDocsHomePage:!1,title:"C. How to change namespace of the PVC",description:"Prerequisites",source:"@site/docs/manual/move_pvc_to_other_namespace.md",sourceDirName:"manual",slug:"/manual/move_pvc_to_other_namespace",permalink:"/xl-release-kubernetes-operator/docs/manual/move_pvc_to_other_namespace",tags:[],version:"current",sidebarPosition:14,frontMatter:{sidebar_position:14},sidebar:"tutorialSidebar",previous:{title:"B. How to change namespace in case there is release already running in the default namespace - with downtime",permalink:"/xl-release-kubernetes-operator/docs/manual/change-namespace-for-xlr-10.3-with-downtime"},next:{title:"Manual helm to operator upgrade of xlr from version 10 to above 22.1 version.",permalink:"/xl-release-kubernetes-operator/docs/manual/manual-upgrade-for-xlr-10"}},m=[{value:"Prerequisites",id:"prerequisites",children:[],level:2},{value:"C.1. Backup everything",id:"c1-backup-everything",children:[],level:2},{value:"C.2. Be sure to not delete PVs with your actions",id:"c2-be-sure-to-not-delete-pvs-with-your-actions",children:[],level:2},{value:"C.3. Stop everything that is using XLR PVC-s (and other PVC if needed)",id:"c3-stop-everything-that-is-using-xlr-pvc-s-and-other-pvc-if-needed",children:[],level:2},{value:"C.4. Move existing PVC to the custom namespace",id:"c4-move-existing-pvc-to-the-custom-namespace",children:[{value:"C.4.OPTION_1 Create PVC in the custom namespace by copying PV data",id:"c4option_1-create-pvc-in-the-custom-namespace-by-copying-pv-data",children:[],level:3},{value:"C.4.OPTION_2 Move existing PVC to the custom namespace by reusing PV",id:"c4option_2-move-existing-pvc-to-the-custom-namespace-by-reusing-pv",children:[],level:3},{value:"C.4.OPTION_3 Clone existing PVC to the custom namespace by CSI Volume Cloning",id:"c4option_3-clone-existing-pvc-to-the-custom-namespace-by-csi-volume-cloning",children:[],level:3}],level:2}],c={toc:m};function u(e){var a=e.components,t=(0,l.Z)(e,i);return(0,r.kt)("wrapper",(0,n.Z)({},c,t,{components:a,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"c-how-to-change-namespace-of-the-pvc"},"C. How to change namespace of the PVC"),(0,r.kt)("h2",{id:"prerequisites"},"Prerequisites"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"The kubectl command-line tool"),(0,r.kt)("li",{parentName:"ul"},"Access to a Kubernetes cluster with installed Release in the ",(0,r.kt)("inlineCode",{parentName:"li"},"default")," namespace")),(0,r.kt)("p",null,"Tested with:"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"xl-release 10.3.9, 22.1.1"),(0,r.kt)("li",{parentName:"ul"},"xl-cli 22.1.1"),(0,r.kt)("li",{parentName:"ul"},"Azure cluster")),(0,r.kt)("h2",{id:"c1-backup-everything"},"C.1. Backup everything"),(0,r.kt)("div",{className:"admonition admonition-caution alert alert--warning"},(0,r.kt)("div",{parentName:"div",className:"admonition-heading"},(0,r.kt)("h5",{parentName:"div"},(0,r.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,r.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",viewBox:"0 0 16 16"},(0,r.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M8.893 1.5c-.183-.31-.52-.5-.887-.5s-.703.19-.886.5L.138 13.499a.98.98 0 0 0 0 1.001c.193.31.53.501.886.501h13.964c.367 0 .704-.19.877-.5a1.03 1.03 0 0 0 .01-1.002L8.893 1.5zm.133 11.497H6.987v-2.003h2.039v2.003zm0-3.004H6.987V5.987h2.039v4.006z"}))),"caution")),(0,r.kt)("div",{parentName:"div",className:"admonition-content"},(0,r.kt)("p",{parentName:"div"},"Before doing any of the following steps backup everything:"),(0,r.kt)("ul",{parentName:"div"},(0,r.kt)("li",{parentName:"ul"},"database data"),(0,r.kt)("li",{parentName:"ul"},"any custom configuration that was done for the operator setup",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"StatefulSets"),(0,r.kt)("li",{parentName:"ul"},"Deployments"),(0,r.kt)("li",{parentName:"ul"},"ConfigMaps"),(0,r.kt)("li",{parentName:"ul"},"Secrets"),(0,r.kt)("li",{parentName:"ul"},"CustomResource"),(0,r.kt)("li",{parentName:"ul"},"anything else that was customized"))),(0,r.kt)("li",{parentName:"ul"},"any volume related to release in the default namespace, for example data from the mounted volumes on the release pod:",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"/opt/xebialabs/xl-release-server/reports"),(0,r.kt)("li",{parentName:"ul"},"/opt/xebialabs/xl-release-server/ext"),(0,r.kt)("li",{parentName:"ul"},"/opt/xebialabs/xl-release-server/conf")))))),(0,r.kt)("h2",{id:"c2-be-sure-to-not-delete-pvs-with-your-actions"},"C.2. Be sure to not delete PVs with your actions"),(0,r.kt)("p",null,"Patch the all PVs to set the \u201cpersistentVolumeReclaimPolicy\u201d to \u201cRetain\u201d, for example (if cluster admin's didn't do that already):"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'\u276f kubectl get pv\nNAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                 STORAGECLASS                                   REASON   AGE\npvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            Delete           Bound    default/dai-xlr-digitalai-release   vp-azure-aks-test-cluster-file-storage-class            6h36m\n...\n\n\u276f kubectl patch pv pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf -p \'{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}\'\npersistentvolume/pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf patched\n')),(0,r.kt)("p",null,"Export the current PVCs objects because it will be necessary to recreate the PVCs in a later stage:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\u276f kubectl get pvc dai-xlr-digitalai-release -n default -o yaml > pvc-dai-xlr-digitalai-release.yaml\n")),(0,r.kt)("p",null,"Iterate on all PVs that are connected to the XLR PVCs in the default namespace, list depends on the installed components.\nFor example, here is list of PVCs that are usually in the default namespace:"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"dai-xlr-digitalai-release"),(0,r.kt)("li",{parentName:"ul"},"data-dai-xlr-postgresql-0"),(0,r.kt)("li",{parentName:"ul"},"data-dai-xlr-rabbitmq-0")),(0,r.kt)("p",null,"On the end check if all PVs have correct Reclaim Policy:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\u276f kubectl get pv\nNAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                      STORAGECLASS                                   REASON   AGE\npvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            Retain           Bound    default/ai-xlr-digitalai-release           vp-azure-aks-test-cluster-file-storage-class            7h\n...\n")),(0,r.kt)("h2",{id:"c3-stop-everything-that-is-using-xlr-pvc-s-and-other-pvc-if-needed"},"C.3. Stop everything that is using XLR PVC-s (and other PVC if needed)"),(0,r.kt)("div",{className:"admonition admonition-caution alert alert--warning"},(0,r.kt)("div",{parentName:"div",className:"admonition-heading"},(0,r.kt)("h5",{parentName:"div"},(0,r.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,r.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",viewBox:"0 0 16 16"},(0,r.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M8.893 1.5c-.183-.31-.52-.5-.887-.5s-.703.19-.886.5L.138 13.499a.98.98 0 0 0 0 1.001c.193.31.53.501.886.501h13.964c.367 0 .704-.19.877-.5a1.03 1.03 0 0 0 .01-1.002L8.893 1.5zm.133 11.497H6.987v-2.003h2.039v2.003zm0-3.004H6.987V5.987h2.039v4.006z"}))),"caution")),(0,r.kt)("div",{parentName:"div",className:"admonition-content"},(0,r.kt)("p",{parentName:"div"},"Be sure that you did backup of the CR before this step!"))),(0,r.kt)("p",null,"If you are sure that everything is backuped and ready for installation on the new custom namespace, you can destroy previous setup on the ",(0,r.kt)("inlineCode",{parentName:"p"},"default")," namespace,\nhere are steps how to do that:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"# get the CR on default namespace and delete it\n\u276f kubectl get digitalaireleases.xlr.digital.ai dai-xlr -n default -o yaml > cr-dai-xlr-default.yaml\n\u276f kubectl delete -n default -f cr-dai-xlr-default.yaml\n\n# get the deployment on default namespace and delete it\n\u276f kubectl get deployment -n default\n\u276f kubectl delete -n default deployment xlr-operator-controller-manager\n\n# get the service on default namespace and delete it\n\u276f kubectl get service -n default\n\u276f kubectl delete -n default service xlr-operator-controller-manager-metrics-service\n\n# get the role on default namespace and delete it\n\u276f kubectl get roles -n default\n\u276f kubectl delete -n default roles xlr-operator-leader-election-role\n\n# get the roleBinding on default namespace and delete it\n\u276f kubectl get roleBinding -n default\n\u276f kubectl delete -n default roleBinding xlr-operator-leader-election-rolebinding\n\n# get clusterRoles related to XLR on default namespace and delete them\n\u276f kubectl get clusterRoles\n\u276f kubectl delete clusterRoles xlr-operator-manager-role xlr-operator-metrics-reader xlr-operator-proxy-role\n\n# get clusterRoleBinding related to XLR on default namespace and delete them\n\u276f kubectl get clusterRoleBinding\n\u276f kubectl delete clusterRoleBinding xlr-operator-proxy-rolebinding xlr-operator-manager-rolebinding\n")),(0,r.kt)("p",null,"Do not delete PVs or PVCs we can reuse them on the new namespace."),(0,r.kt)("h2",{id:"c4-move-existing-pvc-to-the-custom-namespace"},"C.4. Move existing PVC to the custom namespace"),(0,r.kt)("p",null,"Select one option that the best suites for your case."),(0,r.kt)("p",null,"Iterate one of the options on all PVs and PVCs that are connected to the XLR PVCs in the default namespace, list depends on the installed components.\nFor example, here is list of PVCs that are usually in the default namespace:"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"dai-xlr-digitalai-release"),(0,r.kt)("li",{parentName:"ul"},"data-dai-xlr-postgresql-0"),(0,r.kt)("li",{parentName:"ul"},"data-dai-xlr-rabbitmq-0")),(0,r.kt)("h3",{id:"c4option_1-create-pvc-in-the-custom-namespace-by-copying-pv-data"},"C.4.OPTION_1 Create PVC in the custom namespace by copying PV data"),(0,r.kt)("p",null,"Make the copy of the ",(0,r.kt)("inlineCode",{parentName:"p"},"pvc-dai-xlr-digitalai-release.yaml")," for the later reference.\nEdit file ",(0,r.kt)("inlineCode",{parentName:"p"},"pvc-dai-xlr-digitalai-release.yaml"),":"),(0,r.kt)("ol",null,(0,r.kt)("li",{parentName:"ol"},"Delete all the lines under sections:")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"status")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"spec.volumneMode")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"spec.volumneName")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.uid")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.resourceVersion")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.ownerReferences")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.namespace")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.creationTimestamp")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.finalizers")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.annotations.pv.kubernetes.io/bind-completed")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.annotations.pv.kubernetes.io/bound-by-controller"))),(0,r.kt)("ol",{start:2},(0,r.kt)("li",{parentName:"ol"},"Rename following lines by adding namespace name:")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.name")," from dai-xlr-digitalai-release to dai-xlr-custom-namespace-1-digitalai-release"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.labels.release")," from dai-xlr to dai-xlr-custom-namespace-1"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.annotations.meta.helm.sh/release-namespace")," from default to custom-namespace-1"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.annotations.meta.helm.sh/release-name")," from dai-xlr to dai-xlr-custom-namespace-1\nThe renaming rule is to replace any occurrence of ",(0,r.kt)("inlineCode",{parentName:"li"},"dai-xlr")," with ",(0,r.kt)("inlineCode",{parentName:"li"},"dai-xlr-{{custom_namespace_name}}"))),(0,r.kt)("p",null,"Create those PVCs, but inside the Namespace \u201ccustom-namespace-1\u201d:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl apply -f pvc-dai-xlr-digitalai-release.yaml -n custom-namespace-1\npersistentvolumeclaim/dai-xlr-digitalai-release created\n")),(0,r.kt)("ol",{start:3},(0,r.kt)("li",{parentName:"ol"},"Check if PVC is bound\nCheck the PVCs state, which will probably in Pending state, and after some time in Bound state:")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl get pvc -n custom-namespace-1\nNAME                                           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                                   AGE\ndai-xlr-custom-namespace-1-digitalai-release   Bound    pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            vp-azure-aks-test-cluster-file-storage-class   3m33s\n")),(0,r.kt)("p",null,"Start following pod:"),(0,r.kt)("ol",null,(0,r.kt)("li",{parentName:"ol"},"Put following in file ",(0,r.kt)("inlineCode",{parentName:"li"},"pod-dai-pv-access-custom-namespace-1.yaml")," (don't forget to update custom-namespace-1 with real namespace name):")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-yaml"},'apiVersion: v1\nkind: Pod\nmetadata:\n  name: dai-pv-access-custom-namespace-1\nspec:\n  containers:\n    - name: sleeper\n      command: ["sleep", "1d"]\n      image: xebialabs/tiny-tools:22.2.0\n      imagePullPolicy: Always\n      volumeMounts:\n        - mountPath: /opt/xebialabs/xl-release-server/reports\n          name: reports-dir\n          subPath: reports\n        - mountPath: /opt/xebialabs/xl-release-server/work\n          name: reports-dir\n          subPath: work\n        - mountPath: /opt/xebialabs/xl-release-server/conf\n          name: reports-dir\n          subPath: conf\n        - mountPath: /opt/xebialabs/xl-release-server/ext\n          name: reports-dir\n          subPath: ext\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix\n          name: reports-dir\n          subPath: hotfix\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix/lib\n          name: reports-dir\n          subPath: lib\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix/plugins\n          name: reports-dir\n          subPath: plugins\n        - mountPath: /opt/xebialabs/xl-release-server/log\n          name: reports-dir\n          subPath: log\n  restartPolicy: Never\n  volumes:\n    - name: reports-dir\n      persistentVolumeClaim:\n        claimName: dai-xlr-custom-namespace-1-digitalai-release\n')),(0,r.kt)("p",null,"Update the claimName with correct name!"),(0,r.kt)("ol",{start:2},(0,r.kt)("li",{parentName:"ol"},"Start the pod")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl apply -f pod-dai-pv-access-custom-namespace-1.yaml -n custom-namespace-1\n")),(0,r.kt)("ol",{start:3},(0,r.kt)("li",{parentName:"ol"},"Put following in file ",(0,r.kt)("inlineCode",{parentName:"li"},"pod-dai-pv-access.yaml")," for the default namespace:")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-yaml"},'apiVersion: v1\nkind: Pod\nmetadata:\n  name: dai-pv-access\nspec:\n  containers:\n    - name: sleeper\n      command: ["sleep", "1d"]\n      image: xebialabs/tiny-tools:22.2.0\n      imagePullPolicy: Always\n      volumeMounts:\n        - mountPath: /opt/xebialabs/xl-release-server/reports\n          name: reports-dir\n          subPath: reports\n        - mountPath: /opt/xebialabs/xl-release-server/work\n          name: reports-dir\n          subPath: work\n        - mountPath: /opt/xebialabs/xl-release-server/conf\n          name: reports-dir\n          subPath: conf\n        - mountPath: /opt/xebialabs/xl-release-server/ext\n          name: reports-dir\n          subPath: ext\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix\n          name: reports-dir\n          subPath: hotfix\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix/lib\n          name: reports-dir\n          subPath: lib\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix/plugins\n          name: reports-dir\n          subPath: plugins\n        - mountPath: /opt/xebialabs/xl-release-server/log\n          name: reports-dir\n          subPath: log\n  restartPolicy: Never\n  volumes:\n    - name: reports-dir\n      persistentVolumeClaim:\n        claimName: dai-xlr-digitalai-release\n')),(0,r.kt)("ol",{start:4},(0,r.kt)("li",{parentName:"ol"},"Start the pod")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl apply -f pod-dai-pv-access.yaml -n default\n")),(0,r.kt)("ol",{start:5},(0,r.kt)("li",{parentName:"ol"},"Copy data from one pod to ")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"kubectl exec -n default dai-pv-access -- tar cf - \\\n    /opt/xebialabs/xl-release-server/ext \\\n    /opt/xebialabs/xl-release-server/reports \\\n    | kubectl exec -n custom-namespace-1 -i dai-pv-access-custom-namespace-1 -- tar xvf - -C /\n")),(0,r.kt)("ol",{start:6},(0,r.kt)("li",{parentName:"ol"},"Chmod of the moved folder")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"kubectl exec -n custom-namespace-1 -i dai-pv-access-custom-namespace-1 -- chmod -R 777 /opt/xebialabs/xl-release-server/reports/\nkubectl exec -n custom-namespace-1 -i dai-pv-access-custom-namespace-1 -- chmod -R 777 /opt/xebialabs/xl-release-server/ext/\n")),(0,r.kt)("ol",{start:7},(0,r.kt)("li",{parentName:"ol"},"Delete the pods")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl delete pod dai-pv-access-custom-namespace-1 -n custom-namespace-1\n\u276f kubectl delete pod dai-pv-access -n default\n")),(0,r.kt)("h3",{id:"c4option_2-move-existing-pvc-to-the-custom-namespace-by-reusing-pv"},"C.4.OPTION_2 Move existing PVC to the custom namespace by reusing PV"),(0,r.kt)("p",null,"Following option will reuse PV in the new namespace, rollback of the option is more complicated. "),(0,r.kt)("p",null,"Delete the current PVC in the namespace ",(0,r.kt)("inlineCode",{parentName:"p"},"default")," if it still exists (on older version from 22.2 dai-xlr-digitalai-release PVC will not exist):"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\u276f kubectl delete pvc dai-xlr-digitalai-release -n default\n")),(0,r.kt)("p",null,"See that the related PV Status will be changed from ",(0,r.kt)("inlineCode",{parentName:"p"},"Bound")," to ",(0,r.kt)("inlineCode",{parentName:"p"},"Released"),":"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\u276f kubectl get pv pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf\nNAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM                                 STORAGECLASS                                   REASON   AGE\npvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            Retain           Released   digitalai/dai-xlr-digitalai-release   vp-azure-aks-test-cluster-file-storage-class            7h36m\n")),(0,r.kt)("p",null,"Edit each one of the PVs to remove the old references with claim:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\u276f kubectl edit pv pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf\n")),(0,r.kt)("p",null,"Remove lines like following example:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-yaml"},'...\nclaimRef:\n    apiVersion: v1\n    kind: PersistentVolumeClaim\n    name: dai-xlr-digitalai-release\n    namespace: default\n    resourceVersion: "23284462"\n    uid: 53564205-6e1e-45f0-9dcf-e21adefa6eaf\n...\n')),(0,r.kt)("p",null,"Check that there are no references anymore in the CLAIM column:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\u276f kubectl get pv pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf\nNAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS                                   REASON   AGE\npvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            Retain           Available           vp-azure-aks-test-cluster-file-storage-class            8h\n")),(0,r.kt)("p",null,"Make the copy of the ",(0,r.kt)("inlineCode",{parentName:"p"},"pvc-dai-xlr-digitalai-release.yaml")," for the later reference.\nEdit file ",(0,r.kt)("inlineCode",{parentName:"p"},"pvc-dai-xlr-digitalai-release.yaml"),":"),(0,r.kt)("ol",null,(0,r.kt)("li",{parentName:"ol"},"Delete all the lines under section:")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"status")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.namespace")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.uid")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.resourceVersion")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.creationTimestamp")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.finalizers")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.annotations.pv.kubernetes.io/bind-completed")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.annotations.pv.kubernetes.io/bound-by-controller")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.ownerReferences"))),(0,r.kt)("ol",{start:2},(0,r.kt)("li",{parentName:"ol"},"Rename following lines by adding namespace name:")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.name")," from dai-xlr-digitalai-release to dai-xlr-custom-namespace-1-digitalai-release"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.labels.release")," from dai-xlr to dai-xlr-custom-namespace-1"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.annotations.meta.helm.sh/release-namespace")," from default to custom-namespace-1"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"metadata.annotations.meta.helm.sh/release-name")," from dai-xlr to dai-xlr-custom-namespace-1\nThe renaming rule is to replace any occurrence of ",(0,r.kt)("inlineCode",{parentName:"li"},"dai-xlr")," with ",(0,r.kt)("inlineCode",{parentName:"li"},"dai-xlr-{{custom_namespace_name}}"))),(0,r.kt)("p",null,"Create those PVCs again, but inside the Namespace \u201ccustom-namespace-1\u201d:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\u276f kubectl apply -f pvc-dai-xlr-digitalai-release.yaml -n custom-namespace-1\npersistentvolumeclaim/dai-xlr-custom-namespace-1-digitalai-release created\n")),(0,r.kt)("p",null,"Check the PVCs state, which will probably in Pending state, and after some time in Bound state:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\u276f kubectl get pvc -n custom-namespace-1\nNAME                                           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                                   AGE\ndai-xlr-custom-namespace-1-digitalai-release   Bound    pvc-53564205-6e1e-45f0-9dcf-e21adefa6eaf   1Gi        RWO            vp-azure-aks-test-cluster-file-storage-class   3m33s\n")),(0,r.kt)("p",null,"On the moved PV for the release you will need to empty some folders, do that with following pod:"),(0,r.kt)("ol",null,(0,r.kt)("li",{parentName:"ol"},"Put following in file ",(0,r.kt)("inlineCode",{parentName:"li"},"pod-dai-pv-access-custom-namespace-1.yaml")," (don't forget to update custom-namespace-1 with real namespace name):")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-yaml"},'apiVersion: v1\nkind: Pod\nmetadata:\n  name: dai-pv-access-custom-namespace-1\nspec:\n  containers:\n    - name: sleeper\n      command: ["sleep", "1d"]\n      image: xebialabs/tiny-tools:22.2.0\n      imagePullPolicy: Always\n      volumeMounts:\n        - mountPath: /opt/xebialabs/xl-release-server/reports\n          name: reports-dir\n          subPath: reports\n        - mountPath: /opt/xebialabs/xl-release-server/work\n          name: reports-dir\n          subPath: work\n        - mountPath: /opt/xebialabs/xl-release-server/conf\n          name: reports-dir\n          subPath: conf\n        - mountPath: /opt/xebialabs/xl-release-server/ext\n          name: reports-dir\n          subPath: ext\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix\n          name: reports-dir\n          subPath: hotfix\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix/lib\n          name: reports-dir\n          subPath: lib\n        - mountPath: /opt/xebialabs/xl-release-server/hotfix/plugins\n          name: reports-dir\n          subPath: plugins\n        - mountPath: /opt/xebialabs/xl-release-server/log\n          name: reports-dir\n          subPath: log\n  restartPolicy: Never\n  volumes:\n    - name: reports-dir\n      persistentVolumeClaim:\n        claimName: dai-xlr-custom-namespace-1-digitalai-release\n')),(0,r.kt)("ol",{start:2},(0,r.kt)("li",{parentName:"ol"},"Start the pod")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl apply -f pod-dai-pv-access-custom-namespace-1.yaml -n custom-namespace-1\n")),(0,r.kt)("ol",{start:3},(0,r.kt)("li",{parentName:"ol"},"Empty following folders from the pod:")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"/opt/xebialabs/xl-release-server/work"),(0,r.kt)("li",{parentName:"ul"},"/opt/xebialabs/xl-release-server/conf"),(0,r.kt)("li",{parentName:"ul"},"/opt/xebialabs/xl-release-server/hotfix"),(0,r.kt)("li",{parentName:"ul"},"/opt/xebialabs/xl-release-server/hotfix/lib"),(0,r.kt)("li",{parentName:"ul"},"/opt/xebialabs/xl-release-server/hotfix/plugins")),(0,r.kt)("p",null,"Example for the work folder:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},'\u276f kubectl exec -n custom-namespace-1 -i dai-xlr-custom-namespace-1-digitalai-release-0  -- sh -c "rm -fr /opt/xebialabs/xl-release-server/conf/*"\n')),(0,r.kt)("ol",{start:4},(0,r.kt)("li",{parentName:"ol"},"Delete the pod")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl delete pod dai-pv-access-custom-namespace-1 -n custom-namespace-1\n")),(0,r.kt)("p",null,"Iterate on other PVs (for example you can migrate on the same way DB data if you are not using external Postgres, or if you are doing some other way of DB data migration)."),(0,r.kt)("h3",{id:"c4option_3-clone-existing-pvc-to-the-custom-namespace-by-csi-volume-cloning"},"C.4.OPTION_3 Clone existing PVC to the custom namespace by CSI Volume Cloning"),(0,r.kt)("p",null,"Please check following document if this option is possible for your Persisted Volume setup (there are some limitations when it is possible):"),(0,r.kt)("p",null,(0,r.kt)("a",{parentName:"p",href:"https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/"},"CSI Volume Cloning")))}u.isMDXComponent=!0}}]);