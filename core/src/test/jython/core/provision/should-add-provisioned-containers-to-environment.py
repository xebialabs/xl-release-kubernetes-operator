provisioned_container_app_pkg = deployit.importPackage("ProvisionContainersApp/2.0")
yak_server = repository.create(factory.configurationItem('Infrastructure/provisioning-yakserver', 'yak.YakServer', {}))
env = repository.create(
        factory.configurationItem('Environments/provisioning-yakEnv', 'udm.Environment', {'members': [yak_server.id]}))

assertEquals(1, len(env.members))

depl = deployment.prepareInitial(provisioned_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

updatedEnv = repository.read(env.id)
assertEquals(2, len(updatedEnv.members))

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id)

# the step in the task will do the checking because it can only be verified on the server side.
deployit.startTaskAndWait(undeployTask.id)

updatedEnv = repository.read(env.id)
assertEquals(1, len(updatedEnv.members))

# clean up
repository.delete(env.id)
repository.delete(yak_server.id)
repository.delete(env.id + '/ProvisionContainersApp')
repository.delete('Applications/ProvisionContainersApp')