"use strict";(self.webpackChunkdocumentation=self.webpackChunkdocumentation||[]).push([[502],{9611:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return i},contentTitle:function(){return s},metadata:function(){return p},toc:function(){return m},default:function(){return c}});var n=a(7462),r=a(3366),l=(a(7294),a(3905)),o=["components"],i={sidebar_position:10},s="How to change namespace in case there is release already running in the default namespace",p={unversionedId:"manual/change-namespace-for-xlr-10.3",id:"manual/change-namespace-for-xlr-10.3",isDocsHomePage:!1,title:"How to change namespace in case there is release already running in the default namespace",description:"Prerequisites",source:"@site/docs/manual/change-namespace-for-xlr-10.3.md",sourceDirName:"manual",slug:"/manual/change-namespace-for-xlr-10.3",permalink:"/xl-release-kubernetes-operator/docs/manual/change-namespace-for-xlr-10.3",tags:[],version:"current",sidebarPosition:10,frontMatter:{sidebar_position:10},sidebar:"tutorialSidebar",previous:{title:"Setting up custom namespace",permalink:"/xl-release-kubernetes-operator/docs/manual/setting-up-custom-namespace"}},m=[{value:"Prerequisites",id:"prerequisites",children:[],level:2},{value:"Steps to setup operator on the custom namespace",id:"steps-to-setup-operator-on-the-custom-namespace",children:[{value:"1. Create custom namespace",id:"1-create-custom-namespace",children:[],level:3},{value:"3. Prepare the release operator",id:"3-prepare-the-release-operator",children:[],level:3},{value:"5. Update the release operator package to support custom namespace (common part)",id:"5-update-the-release-operator-package-to-support-custom-namespace-common-part",children:[],level:3},{value:"6.a. Update the release operator package to support custom namespace - only in case of Nginx ingress controller",id:"6a-update-the-release-operator-package-to-support-custom-namespace---only-in-case-of-nginx-ingress-controller",children:[],level:3},{value:"6.b. Update the release operator package to support custom namespace - only in case of Haproxy ingress controller",id:"6b-update-the-release-operator-package-to-support-custom-namespace---only-in-case-of-haproxy-ingress-controller",children:[],level:3},{value:"7. Deploy to the cluster custom namespace",id:"7-deploy-to-the-cluster-custom-namespace",children:[],level:3},{value:"8. Apply any custom changes",id:"8-apply-any-custom-changes",children:[],level:3},{value:"9. Wrap-up",id:"9-wrap-up",children:[{value:"9.a Destroy XLR in default namespace",id:"9a-destroy-xlr-in-default-namespace",children:[],level:4}],level:3}],level:2}],d={toc:m};function c(e){var t=e.components,a=(0,r.Z)(e,o);return(0,l.kt)("wrapper",(0,n.Z)({},d,a,{components:t,mdxType:"MDXLayout"}),(0,l.kt)("h1",{id:"how-to-change-namespace-in-case-there-is-release-already-running-in-the-default-namespace"},"How to change namespace in case there is release already running in the default namespace"),(0,l.kt)("h2",{id:"prerequisites"},"Prerequisites"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"The kubectl command-line tool"),(0,l.kt)("li",{parentName:"ul"},"Access to a Kubernetes cluster with installed Release in the ",(0,l.kt)("inlineCode",{parentName:"li"},"default")," namespace")),(0,l.kt)("p",null,"Tested with:"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"xl-deploy 10.3.9"),(0,l.kt)("li",{parentName:"ul"},"xl-release 10.3.9"),(0,l.kt)("li",{parentName:"ul"},"xl-cli 10.3.9"),(0,l.kt)("li",{parentName:"ul"},"Azure cluster")),(0,l.kt)("p",null,"If you have already setup of the XLR default namespace it is possible to move the deployment to the custom namespace. Here we will use for example\n",(0,l.kt)("inlineCode",{parentName:"p"},"custom-namespace-1"),"."),(0,l.kt)("p",null,"In the example we will use XLR 10.3 version with latest 10.3 operator image 10.3.0-407.1129 from the\n",(0,l.kt)("a",{parentName:"p",href:"https://hub.docker.com/r/xebialabsunsupported/release-operator/tags"},"https://hub.docker.com/r/xebialabsunsupported/release-operator/tags")," and latest operator\npackage from the 10.3 branch."),(0,l.kt)("h2",{id:"steps-to-setup-operator-on-the-custom-namespace"},"Steps to setup operator on the custom namespace"),(0,l.kt)("p",null,"With following steps you will setup XLR in the custom namespace, in parallel with running current setup in the ",(0,l.kt)("inlineCode",{parentName:"p"},"default")," namespace."),(0,l.kt)("h3",{id:"1-create-custom-namespace"},"1. Create custom namespace"),(0,l.kt)("p",null,"Setup custom namespace on Kubernetes cluster, ",(0,l.kt)("inlineCode",{parentName:"p"},"custom-namespace-1")," for example:"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre"},"\u276f kubectl create namespace custom-namespace-1\n")),(0,l.kt)("p",null,"Replace ",(0,l.kt)("inlineCode",{parentName:"p"},"custom-namespace-1")," name in this and following steps with your custom namespace name."),(0,l.kt)("h3",{id:"3-prepare-the-release-operator"},"3. Prepare the release operator"),(0,l.kt)("ol",null,(0,l.kt)("li",{parentName:"ol"},"Get the release operator package zip for Azure: deploy-operator-azure-aks-10.3.0-407.1129.zip (operator image is already setup in the package)."),(0,l.kt)("li",{parentName:"ol"},"Unzip the zip with the release operator package."),(0,l.kt)("li",{parentName:"ol"},"Collect all custom changes that are done in the ",(0,l.kt)("inlineCode",{parentName:"li"},"default")," namespace for XLR resources",(0,l.kt)("ul",{parentName:"li"},(0,l.kt)("li",{parentName:"ul"},"StatefulSets"),(0,l.kt)("li",{parentName:"ul"},"Deployments"),(0,l.kt)("li",{parentName:"ul"},"ConfigMaps"),(0,l.kt)("li",{parentName:"ul"},"Secrets"),(0,l.kt)("li",{parentName:"ul"},"CustomResource"),(0,l.kt)("li",{parentName:"ul"},"anything else that was customized"))),(0,l.kt)("li",{parentName:"ol"},"Collect any other change that was done during initial setup according to the\n",(0,l.kt)("a",{parentName:"li",href:"https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#installing-deploy-on-azure-kubernetes-service"},"https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#installing-deploy-on-azure-kubernetes-service")),(0,l.kt)("li",{parentName:"ol"},"If you are using your own database and messaging queue setup, setup it in the same way as in the ",(0,l.kt)("inlineCode",{parentName:"li"},"default")," namespace,\nin the new CR in the release operator package ",(0,l.kt)("inlineCode",{parentName:"li"},"digitalai-release/kubernetes/dairelease_cr.yaml"),"."),(0,l.kt)("li",{parentName:"ol"},"Apply all collected changes from the ",(0,l.kt)("inlineCode",{parentName:"li"},"default")," namespace to the CR in the release operator package ",(0,l.kt)("inlineCode",{parentName:"li"},"digitalai-release/kubernetes/dairelease_cr.yaml"),".\n(The best is to compare new CR ",(0,l.kt)("inlineCode",{parentName:"li"},"digitalai-release/kubernetes/dairelease_cr.yaml")," with the one from the ",(0,l.kt)("inlineCode",{parentName:"li"},"default")," namespace)")),(0,l.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,l.kt)("div",{parentName:"div",className:"admonition-heading"},(0,l.kt)("h5",{parentName:"div"},(0,l.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,l.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,l.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,l.kt)("div",{parentName:"div",className:"admonition-content"},(0,l.kt)("p",{parentName:"div"},"Note:\nAny data migration is out of scope of this document. For example in case of database data migration, check with your DB admins what to do in that case."))),(0,l.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,l.kt)("div",{parentName:"div",className:"admonition-heading"},(0,l.kt)("h5",{parentName:"div"},(0,l.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,l.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,l.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,l.kt)("div",{parentName:"div",className:"admonition-content"},(0,l.kt)("p",{parentName:"div"},"Note:\nCheck if configuration on the new namespace is using same host as on ",(0,l.kt)("inlineCode",{parentName:"p"},"default")," namespace.\nIn that case you will need to execute step 9.a to be able to access XLR pages."))),(0,l.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,l.kt)("div",{parentName:"div",className:"admonition-heading"},(0,l.kt)("h5",{parentName:"div"},(0,l.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,l.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,l.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,l.kt)("div",{parentName:"div",className:"admonition-content"},(0,l.kt)("p",{parentName:"div"},"Note:\nIt would the best that XLR version remains the same as on ",(0,l.kt)("inlineCode",{parentName:"p"},"default")," namespace (to avoid any additional changes in the XLR).\nCompare values in the CR path ",(0,l.kt)("inlineCode",{parentName:"p"},"spec.ImageTag")," and match them to the ",(0,l.kt)("inlineCode",{parentName:"p"},"default")," namespace value.  "))),(0,l.kt)("h3",{id:"5-update-the-release-operator-package-to-support-custom-namespace-common-part"},"5. Update the release operator package to support custom namespace (common part)"),(0,l.kt)("p",null,"Update following files (relative to the provider's directory) with custom namespace name:"),(0,l.kt)("table",null,(0,l.kt)("thead",{parentName:"table"},(0,l.kt)("tr",{parentName:"thead"},(0,l.kt)("th",{parentName:"tr",align:"left"},"File name"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Yaml path"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Value to set"))),(0,l.kt)("tbody",{parentName:"table"},(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/infrastructure.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec","[0]",".children","[0]",".children","[0]",".name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/infrastructure.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec","[0]",".children","[0]",".children","[0]",".namespaceName"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/environment.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec","[0]",".children","[0]",".members","[0]"),(0,l.kt)("td",{parentName:"tr",align:"left"},"~Infrastructure/k8s-infra/xlr/custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/applications.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec","[0]",".children","[0]",".deployables","[7]",".name ="),(0,l.kt)("td",{parentName:"tr",align:"left"},"~Infrastructure/k8s-infra/xlr/custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/cluster-role-digital-proxy-role.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-proxy-role")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/cluster-role-manager-role.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-manager-role")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/cluster-role-metrics-reader.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-metrics-reader")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/leader-election-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"subjects","[0]",".namespace"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/manager-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-manager-rolebinding")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/manager-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"roleRef.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-manager-role")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/manager-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"subjects","[0]",".namespace"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/proxy-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-proxy-rolebinding")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/proxy-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"roleRef.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-proxy-role")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/proxy-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"subjects","[0]",".namespace"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")))),(0,l.kt)("p",null,"In the ",(0,l.kt)("inlineCode",{parentName:"p"},"digitalai-release/applications.yaml")," delete array element from the ",(0,l.kt)("inlineCode",{parentName:"p"},"spec[0].children[0].deployables"),", where name is ",(0,l.kt)("inlineCode",{parentName:"p"},"name: custom-resource-definition"),".\nThis will not deploy again CRD, as it already exists, when it was deployed for the first time."),(0,l.kt)("h3",{id:"6a-update-the-release-operator-package-to-support-custom-namespace---only-in-case-of-nginx-ingress-controller"},"6.a. Update the release operator package to support custom namespace - only in case of Nginx ingress controller"),(0,l.kt)("p",null,"Following changes are in case of usage nginx ingress (default behaviour):"),(0,l.kt)("table",null,(0,l.kt)("thead",{parentName:"table"},(0,l.kt)("tr",{parentName:"thead"},(0,l.kt)("th",{parentName:"tr",align:"left"},"File name"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Yaml path"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Value to set"))),(0,l.kt)("tbody",{parentName:"table"},(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.ingress.annotations.kubernetes.io/ingress.class"),(0,l.kt)("td",{parentName:"tr",align:"left"},"nginx-custom-namespace-1-dai-xlr")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.nginx-ingress-controller.extraArgs.ingress-class"),(0,l.kt)("td",{parentName:"tr",align:"left"},"nginx-custom-namespace-1-dai-xlr")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.nginx-ingress-controller.fullnameOverride"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-dai-xlr-nginx-ingress-controller")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.nginx-ingress-controller.ingressClass"),(0,l.kt)("td",{parentName:"tr",align:"left"},"nginx-custom-namespace-1-dai-xlr")))),(0,l.kt)("h3",{id:"6b-update-the-release-operator-package-to-support-custom-namespace---only-in-case-of-haproxy-ingress-controller"},"6.b. Update the release operator package to support custom namespace - only in case of Haproxy ingress controller"),(0,l.kt)("p",null,"Following changes are in case of usage haproxy ingress:"),(0,l.kt)("table",null,(0,l.kt)("thead",{parentName:"table"},(0,l.kt)("tr",{parentName:"thead"},(0,l.kt)("th",{parentName:"tr",align:"left"},"File name"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Yaml path"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Value to set"))),(0,l.kt)("tbody",{parentName:"table"},(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.ingress.annotations.kubernetes.io/ingress.class"),(0,l.kt)("td",{parentName:"tr",align:"left"},"haproxy-custom-namespace-1-dai-xlr")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.haproxy-ingress.fullnameOverride"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-dai-xlr-haproxy-ingress")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.haproxy-ingress.controller.ingressClass"),(0,l.kt)("td",{parentName:"tr",align:"left"},"haproxy-custom-namespace-1-dai-xlr")))),(0,l.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,l.kt)("div",{parentName:"div",className:"admonition-heading"},(0,l.kt)("h5",{parentName:"div"},(0,l.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,l.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,l.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,l.kt)("div",{parentName:"div",className:"admonition-content"},(0,l.kt)("p",{parentName:"div"},"Note:\nTo setup haproxy instead of default nginx configuration that is provided in the operator package you need to do following changes in the\n",(0,l.kt)("inlineCode",{parentName:"p"},"digitalai-release/kubernetes/dairelease_cr.yaml"),":"),(0,l.kt)("ul",{parentName:"div"},(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"spec.haproxy-ingress.install = true")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"spec.nginx-ingress-controller.install = false")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},'spec.ingress.path = "/xl-release/"')),(0,l.kt)("li",{parentName:"ul"},"in the ",(0,l.kt)("inlineCode",{parentName:"li"},"spec.ingress.annotations")," replace all ",(0,l.kt)("inlineCode",{parentName:"li"},"nginx.")," settings and put:")),(0,l.kt)("pre",{parentName:"div"},(0,l.kt)("code",{parentName:"pre"},'      ingress.kubernetes.io/ssl-redirect: "false"\n      ingress.kubernetes.io/rewrite-target: /\n      ingress.kubernetes.io/affinity: cookie\n      ingress.kubernetes.io/session-cookie-name: JSESSIONID\n      ingress.kubernetes.io/session-cookie-strategy: prefix\n      ingress.kubernetes.io/config-backend: |\n        option httpchk GET /ha/health HTTP/1.0\n')))),(0,l.kt)("h3",{id:"7-deploy-to-the-cluster-custom-namespace"},"7. Deploy to the cluster custom namespace"),(0,l.kt)("ol",null,(0,l.kt)("li",{parentName:"ol"},"Do the step 5 from the documentation ",(0,l.kt)("a",{parentName:"li",href:"https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-6set-up-the-xl-deploy-container-instance"},"Step 5\u2014Download and set up the XL CLI")),(0,l.kt)("li",{parentName:"ol"},"Do the step 6 from the documentation ",(0,l.kt)("a",{parentName:"li",href:"https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-6set-up-the-xl-deploy-container-instance-1"},"Step 6\u2014Set up the XL Deploy Container instance")),(0,l.kt)("li",{parentName:"ol"},"Do the step 7 from the documentation ",(0,l.kt)("a",{parentName:"li",href:"https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-7activate-the-deployment-process-1"},"Step 7\u2014Activate the deployment process")),(0,l.kt)("li",{parentName:"ol"},"Do the step 8 from the documentation ",(0,l.kt)("a",{parentName:"li",href:"https://docs.xebialabs.com/v.10.3/deploy/how-to/k8s-operator/install-deploy-using-k8s-operator/#step-8verify-the-deployment-status-1"},"Step 8\u2014Verify the deployment status"))),(0,l.kt)("h3",{id:"8-apply-any-custom-changes"},"8. Apply any custom changes"),(0,l.kt)("p",null,"If you have any custom changes that you collected previously in the step 3.3, you can apply them again in this step in the same way as before on the ",(0,l.kt)("inlineCode",{parentName:"p"},"default")," namespace."),(0,l.kt)("h3",{id:"9-wrap-up"},"9. Wrap-up"),(0,l.kt)("p",null,"Wait for all pods to ready and without any errors. "),(0,l.kt)("p",null,"If you used same host in the new custom namespace to the one that is on the ",(0,l.kt)("inlineCode",{parentName:"p"},"default")," namespace, in that case XLR page is still opening from the ",(0,l.kt)("inlineCode",{parentName:"p"},"default"),"\nnamespace. You need in that case apply step 9.a, after that on the configurated host will be available XLR that is from the new custom namespace."),(0,l.kt)("p",null,"In case of haproxy and one release pod, list of pods should look like following table:"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre"},"\u2502 NAMESPACE\u2191           NAME                                                          READY     RESTARTS STATUS  \u2502\n\u2502 custom-namespace-1   custom-namespace-1-dai-xlr-haproxy-ingress-7df948c7d7-7xcrt   1/1              0 Running \u2502\n\u2502 custom-namespace-1   dai-xlr-digitalai-release-0                                   1/1              0 Running \u2502\n\u2502 custom-namespace-1   dai-xlr-postgresql-0                                          1/1              0 Running \u2502\n\u2502 custom-namespace-1   dai-xlr-rabbitmq-0                                            1/1              0 Running \u2502\n\u2502 custom-namespace-1   xlr-operator-controller-manager-78ff46dbb8-rq45l              2/2              0 Running \u2502    \n")),(0,l.kt)("h4",{id:"9a-destroy-xlr-in-default-namespace"},"9.a Destroy XLR in default namespace"),(0,l.kt)("p",null,"If you are sure that everything is up and running on the new custom namespace, you can destroy previous setup on the ",(0,l.kt)("inlineCode",{parentName:"p"},"default")," namespace,\nhere are steps how to that:"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-shell"},"# get the CR on default namespace and delete it\n\u276f kubectl get digitalaireleases.xlr.digital.ai dai-xlr -n default -o yaml > dai-xlr-default.yaml\n\u276f kubectl delete -n default -f dai-xlr-default.yaml\n\n# get the deployment on default namespace and delete it\n\u276f kubectl get deployment -n default\n\u276f kubectl delete -n default deployment xlr-operator-controller-manager\n\n# get the service on default namespace and delete it\n\u276f kubectl get service -n default\n\u276f kubectl delete -n default service xlr-operator-controller-manager-metrics-service\n\n# get the role on default namespace and delete it\n\u276f kubectl get roles -n default\n\u276f kubectl delete -n default roles xlr-operator-leader-election-role\n\n# get the roleBinding on default namespace and delete it\n\u276f kubectl get roleBinding -n default\n\u276f kubectl delete -n default roleBinding xlr-operator-leader-election-rolebinding\n\n# get clusterRoles related to XLR on default namespace and delete them\n\u276f kubectl get clusterRoles\n\u276f kubectl delete clusterRoles xlr-operator-manager-role xlr-operator-metrics-reader xlr-operator-proxy-role\n\n# get clusterRoleBinding related to XLR on default namespace and delete them\n\u276f kubectl get clusterRoleBinding\n\u276f kubectl delete clusterRoleBinding xlr-operator-proxy-rolebinding xlr-operator-manager-rolebinding\n\n# get pvcs related to XLR on default namespace and delete them (list of the pvcs depends on what is enabled in the deployment)\n\u276f kubectl get pvc -n default\n\u276f kubectl delete -n default pvc data-dai-xlr-postgresql-0 data-dai-xlr-rabbitmq-0\n")),(0,l.kt)("p",null,"You can also clean up any configmaps or secrets that are in the ",(0,l.kt)("inlineCode",{parentName:"p"},"default")," namespace and related to the XLR."))}c.isMDXComponent=!0}}]);