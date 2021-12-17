#
def createServer(memberSet, name, totalSteps, delaySecs, logKb):
    server = factory.configurationItem("Infrastructure/" + name, "test-v3.DummyJeeServer",{"hostName":"value" + name, "numberOfSteps":str(totalSteps), "stepDelayTimeInMilliSeconds":str(delaySecs), "amountOfKBLogFiles":str(logKb)})
    memberSet.append(repository.create(server).id)
    return

def addHost(memberSet, name):
    host = factory.configurationItem("Infrastructure/" + name, "test-v3.DummyHost", {"os":"UNIX", "address":"localhost", "username":"admin", "password":"admin", "accessMethod":"FTP"})
    memberSet.append(repository.create(host).id)
    return
    
def createEnvs(envName, totalEnvs, envSize, serverName, totalSteps, delaySecs, logKb, addHostToEnv):
    memberSet = []
    for i in range(0,envSize):
        createServer(memberSet, serverName + str(i), totalSteps, delaySecs, logKb)
    if (addHostToEnv):
        addHost(memberSet, "Host-with-" + serverName)

    for i in range(0,totalEnvs) :
        repository.create(factory.configurationItem("Environments/" + str(i) + envName + str(i), "udm.Environment", {'members': memberSet}))
    return

def createApp(appName):
    return repository.create(factory.configurationItem("Applications/" + appName, "udm.Application")).id

def createEar(memberSet, name, filename):
    ear = factory.artifact(name, "test-v3.DummyEar", {},"**********")
    ear.filename = filename
    memberSet.append(repository.create(ear).id)
    return

def createPackages(applicationId, packageName, totalPackages, packageSize, earName):
    for i in range(0, totalPackages) :
        version = str(i+1) + "." + str(i % 10)
        memberSet = []
        packageId = applicationId + "/" + version
        package = factory.configurationItem(packageId, "udm.DeploymentPackage", {'application': applicationId})
        repository.create(package)
        for i in range(0, packageSize) :
            createEar(memberSet, packageId + "/" + earName + str(i), earName + str(i))  
        package.deployables = memberSet
        repository.update(package)
    return

def getDeploymentTask(packageId, environmentId, updateDeployedIds = False):
    deploymentRef = deployment.prepareInitial(packageId, environmentId)
    deploymentRef = deployment.prepareAutoDeployeds(deploymentRef)
    if updateDeployedIds == True:
        for ordinal, deployed in enumerate(deploymentRef.deployeds):
            deployed.id = deployed.id + '(' + str(ordinal + 1) + ')'
    return deployment.createDeployTask(deploymentRef).id

createEnvs("export-hostEnv", 1, 2, "export-hostEnvServer", 20, 1000, 2, True)
createEnvs("export-exportEnv", 3, 1, "export-exportServer", 1, 1000, 5, False)
createPackages(createApp("export-tinyExportApp"), "export-tinyExportApp", 2, 1, "export-tinyExportEar")
createPackages(createApp("export-smallExportApp"), "export-smallExportApp", 4, 2, "export-smallExportEar")

archiveTaskIds = []
packages = [repository.read('Applications/export-tinyExportApp/1.0'), repository.read('Applications/export-smallExportApp/1.0')]
for setupDeploy in [(packages[pid].id,"Environments/%iexport-exportEnv%i" % (eid, eid), (False, True)[eid]) for pid in range(0,2) for eid in range(0,2)]:
    taskId = getDeploymentTask(setupDeploy[0], setupDeploy[1], setupDeploy[2])
    archiveTaskIds.append(taskId)
    deployit.startTaskAndWait(taskId)
