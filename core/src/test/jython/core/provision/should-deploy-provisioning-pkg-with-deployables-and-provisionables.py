provisioning_pkg = deployit.importPackage("ProvisioningApp/1.0")
yak_server = repository.create(factory.configurationItem('Infrastructure/yakserver-provisioning', 'yak.YakServer', {}))
env = repository.create(factory.configurationItem('Environments/yakEnv-provisioning', 'udm.Environment', {'members': [yak_server.id]}))

assertEquals(1, len(env.members))

depl = deployment.prepareInitial(provisioning_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

updatedEnv = repository.read("Environments/yakEnv-provisioning")
assertEquals(3, len(updatedEnv.members))
sortedMembers = sorted(map(lambda x : x, updatedEnv.members))
assertTrue(sortedMembers[1].endswith("yakBucket"))
assertTrue(sortedMembers[2].endswith("yakBucket-2"))

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id)

# the step in the task will do the checking because it can only be verified on the server side.
deployit.startTaskAndWait(undeployTask.id)

updatedEnv = repository.read("Environments/yakEnv-provisioning")
assertEquals(1, len(updatedEnv.members))

# clean up
repository.delete(env.id)
repository.delete(yak_server.id)
repository.delete(env.id + '/ProvisioningApp')
repository.delete('Applications/ProvisioningApp')
