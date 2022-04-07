"use strict";(self.webpackChunkdocumentation=self.webpackChunkdocumentation||[]).push([[753],{1433:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return s},contentTitle:function(){return o},metadata:function(){return p},toc:function(){return m},default:function(){return d}});var n=a(7462),r=a(3366),l=(a(7294),a(3905)),i=["components"],s={sidebar_position:8},o="Setting up custom namespace",p={unversionedId:"manual/setting-up-custom-namespace",id:"manual/setting-up-custom-namespace",isDocsHomePage:!1,title:"Setting up custom namespace",description:"Manual setup (not for OpenShift based provider)",source:"@site/docs/manual/setting-up-custom-namespace.md",sourceDirName:"manual",slug:"/manual/setting-up-custom-namespace",permalink:"/xl-release-kubernetes-operator/docs/manual/setting-up-custom-namespace",tags:[],version:"current",sidebarPosition:8,frontMatter:{sidebar_position:8},sidebar:"tutorialSidebar",previous:{title:"Adding truststore files",permalink:"/xl-release-kubernetes-operator/docs/manual/updating-truststore-files"},next:{title:"How to change namespace in case there is release already running in the default namespace",permalink:"/xl-release-kubernetes-operator/docs/manual/change-namespace-for-xlr-10.3"}},m=[{value:"Manual setup (not for OpenShift based provider)",id:"manual-setup-not-for-openshift-based-provider",children:[{value:"Prerequisites",id:"prerequisites",children:[],level:3},{value:"Create custom namespace",id:"create-custom-namespace",children:[],level:3},{value:"Update the release operator package to support custom namespace",id:"update-the-release-operator-package-to-support-custom-namespace",children:[],level:3}],level:2},{value:"Semi-automatic setup with xl-cli (not for OpenShift based provider)",id:"semi-automatic-setup-with-xl-cli-not-for-openshift-based-provider",children:[{value:"Prerequisites",id:"prerequisites-1",children:[],level:3},{value:"Create custom namespace",id:"create-custom-namespace-1",children:[],level:3},{value:"Update the release operator package to support custom namespace",id:"update-the-release-operator-package-to-support-custom-namespace-1",children:[],level:3}],level:2}],c={toc:m};function d(e){var t=e.components,a=(0,r.Z)(e,i);return(0,l.kt)("wrapper",(0,n.Z)({},c,a,{components:t,mdxType:"MDXLayout"}),(0,l.kt)("h1",{id:"setting-up-custom-namespace"},"Setting up custom namespace"),(0,l.kt)("h2",{id:"manual-setup-not-for-openshift-based-provider"},"Manual setup (not for OpenShift based provider)"),(0,l.kt)("h3",{id:"prerequisites"},"Prerequisites"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Linux environment"),(0,l.kt)("li",{parentName:"ul"},"The kubectl command-line tool"),(0,l.kt)("li",{parentName:"ul"},"Access to a Kubernetes cluster to install Release")),(0,l.kt)("h3",{id:"create-custom-namespace"},"Create custom namespace"),(0,l.kt)("p",null,"Setup custom namespace on Kubernetes cluster, ",(0,l.kt)("inlineCode",{parentName:"p"},"custom-namespace-1")," for example:"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl create namespace custom-namespace-1\n")),(0,l.kt)("h3",{id:"update-the-release-operator-package-to-support-custom-namespace"},"Update the release operator package to support custom namespace"),(0,l.kt)("p",null,"Update following files (relative to the provider's directory) with custom namespace name:"),(0,l.kt)("table",null,(0,l.kt)("thead",{parentName:"table"},(0,l.kt)("tr",{parentName:"thead"},(0,l.kt)("th",{parentName:"tr",align:"left"},"File name"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Yaml path"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Value to set"))),(0,l.kt)("tbody",{parentName:"table"},(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/infrastructure.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec","[0]",".children","[0]",".children","[0]",".name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/infrastructure.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec","[0]",".children","[0]",".children","[0]",".namespaceName"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/environment.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec","[0]",".children","[0]",".members","[0]"),(0,l.kt)("td",{parentName:"tr",align:"left"},"~Infrastructure/k8s-infra/xlr/custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/cluster-role-digital-proxy-role.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-proxy-role")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/cluster-role-manager-role.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-manager-role")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/cluster-role-metrics-reader.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-metrics-reader")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/leader-election-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"subjects","[0]",".namespace"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/manager-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-manager-rolebinding")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/manager-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"roleRef.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-manager-role")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/manager-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"subjects","[0]",".namespace"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/proxy-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"metadata.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-proxy-rolebinding")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/proxy-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"roleRef.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-xlr-operator-proxy-role")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/template/proxy-rolebinding.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"subjects","[0]",".namespace"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1")))),(0,l.kt)("p",null,"Following changes are in case of usage nginx ingress (default behaviour):"),(0,l.kt)("table",null,(0,l.kt)("thead",{parentName:"table"},(0,l.kt)("tr",{parentName:"thead"},(0,l.kt)("th",{parentName:"tr",align:"left"},"File name"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Yaml path"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Value to set"))),(0,l.kt)("tbody",{parentName:"table"},(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.ingress.annotations.kubernetes.io/ingress.class"),(0,l.kt)("td",{parentName:"tr",align:"left"},"nginx-custom-namespace-1-dai-xlr")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.nginx-ingress-controller.extraArgs.ingress-class"),(0,l.kt)("td",{parentName:"tr",align:"left"},"nginx-custom-namespace-1-dai-xlr")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.nginx-ingress-controller.fullnameOverride"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-dai-xlr-nginx-ingress-controller")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.nginx-ingress-controller.ingressClassResource.controllerClass"),(0,l.kt)("td",{parentName:"tr",align:"left"},"k8s.io/ingress-nginx-custom-namespace-1-dai-xlr")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.nginx-ingress-controller.ingressClassResource.name"),(0,l.kt)("td",{parentName:"tr",align:"left"},"nginx-custom-namespace-1-dai-xlr")))),(0,l.kt)("p",null,"Following changes are in case of usage haproxy ingress:"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"spec.haproxy-ingress.install = true")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"spec.nginx-ingress-controller.install = false"))),(0,l.kt)("table",null,(0,l.kt)("thead",{parentName:"table"},(0,l.kt)("tr",{parentName:"thead"},(0,l.kt)("th",{parentName:"tr",align:"left"},"File name"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Yaml path"),(0,l.kt)("th",{parentName:"tr",align:"left"},"Value to set"))),(0,l.kt)("tbody",{parentName:"table"},(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.ingress.annotations.kubernetes.io/ingress.class"),(0,l.kt)("td",{parentName:"tr",align:"left"},"haproxy-custom-namespace-1-dai-xlr")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.haproxy-ingress.fullnameOverride"),(0,l.kt)("td",{parentName:"tr",align:"left"},"custom-namespace-1-dai-xlr-haproxy-ingress")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:"left"},"digitalai-release/kubernetes/dairelease_cr.yaml"),(0,l.kt)("td",{parentName:"tr",align:"left"},"spec.haproxy-ingress.controller.ingressClass"),(0,l.kt)("td",{parentName:"tr",align:"left"},"haproxy-custom-namespace-1-dai-xlr")))),(0,l.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,l.kt)("div",{parentName:"div",className:"admonition-heading"},(0,l.kt)("h5",{parentName:"div"},(0,l.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,l.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,l.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,l.kt)("div",{parentName:"div",className:"admonition-content"},(0,l.kt)("p",{parentName:"div"},"Note:"),(0,l.kt)("ul",{parentName:"div"},(0,l.kt)("li",{parentName:"ul"},"This setup is not for OpenShift based provider."),(0,l.kt)("li",{parentName:"ul"},"If you are just setting up one Release on the cluster: you could omit changes related to the renaming cluster roles, but that is not recommended because\nof consistency and if you in future will require starting additional Release on the same cluster (in other namespace) you will have problems with cluster naming collisions")))),(0,l.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,l.kt)("div",{parentName:"div",className:"admonition-heading"},(0,l.kt)("h5",{parentName:"div"},(0,l.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,l.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,l.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,l.kt)("div",{parentName:"div",className:"admonition-content"},(0,l.kt)("p",{parentName:"div"},"If you already have on the cluster CRD ",(0,l.kt)("inlineCode",{parentName:"p"},"digitalaireleases.xlr.digital.ai"),", in that case you need to skip installation of the CRD again on the cluster.\nThat CRD already exists on the cluster if you have on the same cluster installation of the Release in some other namespace.\nTo check existence of the CRD run:"),(0,l.kt)("pre",{parentName:"div"},(0,l.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl get crd\nNAME                                             CREATED AT\ndigitalaireleases.xlr.digital.ai                 2022-03-31T19:03:30Z\n")),(0,l.kt)("p",{parentName:"div"},"To do that remove from the file ",(0,l.kt)("inlineCode",{parentName:"p"},"digitalai-release/applications.yaml")," section that is under path ",(0,l.kt)("inlineCode",{parentName:"p"},"spec[0].children[0].deployables[7]"),"\n(it is section with ",(0,l.kt)("inlineCode",{parentName:"p"},"name: custom-resource-definition"),")."))),(0,l.kt)("p",null,"After setup, you can continue with standard deployment of the Release to the Kubernetes cluster."),(0,l.kt)("h2",{id:"semi-automatic-setup-with-xl-cli-not-for-openshift-based-provider"},"Semi-automatic setup with xl-cli (not for OpenShift based provider)"),(0,l.kt)("h3",{id:"prerequisites-1"},"Prerequisites"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Linux environment"),(0,l.kt)("li",{parentName:"ul"},"The kubectl command-line tool"),(0,l.kt)("li",{parentName:"ul"},"The yq command-line tool (",(0,l.kt)("a",{parentName:"li",href:"https://github.com/mikefarah/yq/releases"},"Use the latest binary"),")"),(0,l.kt)("li",{parentName:"ul"},"The xl-cli (currently only nightly release has supported feature)"),(0,l.kt)("li",{parentName:"ul"},"Access to a Kubernetes cluster to install Release")),(0,l.kt)("h3",{id:"create-custom-namespace-1"},"Create custom namespace"),(0,l.kt)("p",null,"Setup custom namespace on Kubernetes cluster, ",(0,l.kt)("inlineCode",{parentName:"p"},"custom-namespace-2")," for example:"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl create namespace custom-namespace-2\n")),(0,l.kt)("h3",{id:"update-the-release-operator-package-to-support-custom-namespace-1"},"Update the release operator package to support custom namespace"),(0,l.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,l.kt)("div",{parentName:"div",className:"admonition-heading"},(0,l.kt)("h5",{parentName:"div"},(0,l.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,l.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,l.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,l.kt)("div",{parentName:"div",className:"admonition-content"},(0,l.kt)("p",{parentName:"div"},"In case of haproxy ingress setup, you need first to setup everything what is needed for haproxy ingress:"),(0,l.kt)("ul",{parentName:"div"},(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"spec.haproxy-ingress.install = true")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"spec.nginx-ingress-controller.install = false")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"spec.ingress.annotations.kubernetes.io/ingress.class = haproxy"))))),(0,l.kt)("p",null,"Instead of updating manually YAML files in the operator package, you can update them by running xl-cli: "),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-shell"},"xl op --change-namespace\n? Select the Kubernetes setup where the digitalai Devops Platform will be installed or uninstalled: AzureAKS [Azure AKS]\n? Do you want to use Kubernetes' current-context from ~/.kube/config? Yes\n? Do you want to use an existing Kubernetes namespace? Yes\n? Enter the name of the existing Kubernetes namespace where the XebiaLabs DevOps Platform will be installed, updated or undeployed: custom-namespace-2\n? Product server you want to clean. daiRelease\n? Does product custom resource definition already exists on the cluster. No\n? Enter path to the operator package. /xl/master/xl-release-kubernetes-operator\nEverything has been updated!\n")),(0,l.kt)("p",null,"From the questions, last 2 could be interesting:"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"? Does product custom resource definition already exists on the cluster. (y/N)"),"\nThis is question about should product installation create CRD ",(0,l.kt)("inlineCode",{parentName:"li"},"digitalaireleases.xlr.digital.ai"),".\nCheck if on the cluster there is already specified CRD. If there is the CRD in that case answer with ",(0,l.kt)("inlineCode",{parentName:"li"},"y")," to skip CRD installation. For example:")),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-shell"},"\u276f kubectl get crd\nNAME                                             CREATED AT\ndigitalaireleases.xlr.digital.ai                 2022-03-31T19:03:30Z\n")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"? Enter path to the operator package."),"\nFor this answer you need specify path to the unzipped operator package")))}d.isMDXComponent=!0}}]);