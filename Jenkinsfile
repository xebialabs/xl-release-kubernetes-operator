pipeline {
    agent none
    parameters {
        choice(name: 'PRODUCT', choices: ['XL Release', 'XL Deploy'], description: 'Select the product to package')
        choice(name: 'PUSH_TO_NEXUS', choices: ['No', 'Yes'], description: 'Do you want to push artifacts to XebiaLabs Nexus?')
        choice(name: 'PUSH_TO_DIST', choices: ['No', 'Yes'], description: 'Do you want to push artifacts to XebiaLabs dist?')
        string(name: 'OPERATOR_VERSION', defaultValue: '', description: 'Specify the version of the operator to be released.')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Specify the branch from which the release will be performed.')
    }
    environment {
        NEXUS_VERSION = "nexus3"
        NEXUS_PROTOCOL = "http"
        NEXUS_PASSWORD = credentials('nexus-ci')
        XEBIA_DIST_PASSWORD = credentials('16717ee9-bee2-4eb4-ab9e-022ff33a75ef')
        GitHubUser= credentials('XebiaLabsCIGithubToken')
        NEXUS_URL= 'https://nexus.xebialabs.com/nexus/content/repositories/releases/com/xebialabs/operator-based-installer'
    }
    stages {
        stage('Git clone and zip') {
            when {
                anyOf {
                    expression { params.PRODUCT == 'XL Deploy' }
                    expression { params.PRODUCT == 'XL Release' }
                }
            }
            agent {
                node {
                    label "xlp-helm"
                }
            }
            steps {
                step([$class: 'WsCleanup'])
                checkout scm
                script {
                    if ( params.PRODUCT == 'XL Release' ) {
                        //sh "rm -rf /var/lib/jenkins/workspace/XL Operator"
                        sh "git clone http://$GitHubUser_USR:$GitHubUser_PSW@github.com/xebialabs/xl-release-kubernetes-operator.git -b $BRANCH"
                        dir("xl-release-kubernetes-operator") {
                            sh 'for r in */; do zip -r "${r%/}-$OPERATOR_VERSION.zip" "$r"; done'
                            sh "ls -lah"
                        }
                        echo "Repository `xl-release-kubernetes-operator` has been successfully checked out"
                    } else {
                        //sh "rm -rf /var/lib/jenkins/workspace/XL Operator"
                        sh "git clone http://$GitHubUser_USR:$GitHubUser_PSW@github.com/xebialabs/xl-deploy-kubernetes-operator.git -b $BRANCH"
                        dir("xl-deploy-kubernetes-operator") {
                            sh 'for r in */; do zip -r "${r%/}-$OPERATOR_VERSION.zip" "$r"; done'
                            sh "ls -lah"
                        }
                        echo "Repository `xl-deploy-kubernetes-operator` has been successfully checked out"
                    }
                }
            }
        }
        stage('Push to Nexus repository') {
            when {
                anyOf {
                    expression { params.PUSH_TO_NEXUS == 'Yes' && params.PRODUCT == 'XL Deploy' }
                    expression { params.PUSH_TO_NEXUS == 'Yes' && params.PRODUCT == 'XL Release' }
                }
            }
            agent {
                node {
                    label "xlp-helm"
                }
            }
            steps {
                script {
                    if (params.PRODUCT == 'XL Release') {
                        dir("xl-release-kubernetes-operator") {
                            echo "Pushing the Release Operator artifacts to Nexus"
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file release-operator-aws-ek*.zip ${NEXUS_URL}/Release/'
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file release-operator-az*.zip ${NEXUS_URL}/Release/'
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file release-operator-open*.zip ${NEXUS_URL}/Release/'
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file release-operator-onpr*.zip ${NEXUS_URL}/Release/'
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file release-operator-gcp-gk*.zip ${NEXUS_URL}/Release/'

                            echo "Push successful"
                        }
                    } else {
                        dir("xl-deploy-kubernetes-operator") {
                            echo "Pushing Deploy Operator artifacts to Nexus"
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file deploy-operator-aws-ek*.zip ${NEXUS_URL}/Deploy/'
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file deploy-operator-az*.zip ${NEXUS_URL}/Deploy/'
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file deploy-operator-open*.zip ${NEXUS_URL}/Deploy/'
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file deploy-operator-onpr*.zip ${NEXUS_URL}/Deploy/'
                            sh  'curl -v -k -u ${NEXUS_PASSWORD} --upload-file deploy-operator-gcp-gk*.zip ${NEXUS_URL}/Deploy/'
                            echo "Push successful"
                        }
                    }
                }
            }
        }
        stage('Nexus to dist server') {
            when {
                anyOf {
                    expression { params.PUSH_TO_DIST == 'Yes' && params.PRODUCT == 'XL Deploy' }
                    expression { params.PUSH_TO_DIST == 'Yes' && params.PRODUCT == 'XL Release'}

                }
            }
            agent {
                node {
                    label "xlp-helm"
                }
            }
            steps {
                script {
                     if (params.PRODUCT == 'XL Release') {
                        dir("xl-release-kubernetes-operator") {
                           echo "Pushing Release Operator artifacts to XebiaLabs distribution"
                           sh "ssh xebialabs@nexus1.xebialabs.cyso.net rsync --update -raz -i --include='release-operator-aws-eks-*.zip' --include='release-operator-azure-aks-*.zip' --include='release-operator-openshift-*.zip' --include='release-operator-onprem-*.zip' --include='release-operator-gcp-gke-*.zip'  --exclude='*'  /opt/sonatype-work/nexus/storage/releases/com/xebialabs/operator-based-installer/Release/ xldown@dist.xebialabs.com:/var/www/dist.xebialabs.com/customer/operator/release"
                        }
                    } else {
                        dir("xl-deploy-kubernetes-operator") {
                            echo "Pushing Deploy Operator artifacts to XebiaLabs distribution"
                            sh "ssh xebialabs@nexus1.xebialabs.cyso.net rsync --update -raz -i --include='deploy-operator-aws-eks-*.zip' --include='deploy-operator-azure-aks-*.zip' --include='deploy-operator-openshift-*.zip' --include='deploy-operator-onprem-*.zip' --include='deploy-operator-gcp-gke-*.zip' --exclude='*' /opt/sonatype-work/nexus/storage/releases/com/xebialabs/operator-based-installer/Deploy/ xldown@dist.xebialabs.com:/var/www/dist.xebialabs.com/customer/operator/deploy"
                        }
                    }
                }
            }
        }
    }
}
