provisioned_container_app_pkg = deployit.importPackage("ProvisionedContainersApp/1.0")
yak_server = repository.create(factory.configurationItem('Infrastructure/yakserver-cardinality', 'yak.YakServer', {}))
env = repository.create(
        factory.configurationItem('Environments/yakEnv-cardinality', 'udm.Environment', {'members': [yak_server.id]}))

assertEquals(1, len(env.members))

depl = deployment.prepareInitial(provisioned_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

updatedEnv = repository.read("Environments/yakEnv-cardinality")

assertEquals(3, len(updatedEnv.dictionaries))
sortedDict = sorted(map(lambda x : x, updatedEnv.dictionaries))
assertTrue(sortedDict[0].endswith("udmdic"))
assertTrue(sortedDict[1].endswith("udmdic-2"))

assertEquals(4, len(updatedEnv.members))
sortedMembers = sorted(map(lambda x : x, updatedEnv.members))
assertTrue(sortedMembers[1].endswith("yakBucket"))
assertTrue(sortedMembers[2].endswith("yakBucket-2"))

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id)

# the step in the task will do the checking because it can only be verified on the server side.
deployit.startTaskAndWait(undeployTask.id)

updatedEnv = repository.read("Environments/yakEnv-cardinality")
assertEquals(1, len(updatedEnv.members))
assertEquals(0, len(updatedEnv.dictionaries))

# clean up
repository.delete(env.id)
repository.delete(yak_server.id)
repository.delete(env.id + '/ProvisionedContainersApp')
repository.delete('Applications/ProvisionedContainersApp/1.0')
