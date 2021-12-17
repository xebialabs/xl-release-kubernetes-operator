provisioned_container_app_pkg = deployit.importPackage("ProvisionedContainersApp/2.0")
yak_server = repository.create(factory.configurationItem('Infrastructure/yakserver-provisioned', 'yak.YakServer', {}))
env = repository.create(
    factory.configurationItem('Environments/yakEnv6', 'udm.Environment', {'members': [yak_server.id]}))

assertEquals(1, len(env.members))

depl = deployment.prepareInitial(provisioned_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

provisioned1 = repository.read("Infrastructure/yakserver-provisioned/yakBucket-1")
assertNotNone(provisioned1)
provisioned2 = repository.read("Infrastructure/yakserver-provisioned/yakBucket-2-2")
assertNotNone(provisioned2)

# clean up
repository.delete(env.id)
repository.delete(yak_server.id)
repository.delete(env.id + '/ProvisionedContainersApp')
repository.delete('Applications/ProvisionedContainersApp/2.0')
