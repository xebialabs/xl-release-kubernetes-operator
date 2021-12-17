provisioned_container_app_pkg = deployit.importPackage("ProvisionedContainersApp/4.0")
env_id = 'Environments/yakEnv-placeholders_from_map'
yak_server = repository.create(factory.configurationItem('Infrastructure/best-yakserver-placeholders_from_map', 'yak.YakServer', {}))
env = repository.create(factory.configurationItem(env_id, 'udm.Environment', {'members': [yak_server.id]}))

assertEquals(1, len(env.members))

depl = deployment.prepareInitial(provisioned_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

dict1 = repository.read("Environments/mydict")
assertNotNone(dict1)

# The entries in dictionary are resolved from the contextual place holder - {{%mapoutput.foo%}} and {{%mapoutput.fiz%}}
assertEquals(dict1.entries['foo'], "bar")
assertEquals(dict1.entries['fiz'], "buz")

provisioned1 = repository.read("Infrastructure/best-yakserver-placeholders_from_map/yakBucket-mapOutput")
assertNotNone(provisioned1)

# clean up
repository.delete(env.id)
repository.delete(yak_server.id)
repository.delete(env.id + '/ProvisionedContainersApp')
repository.delete('Applications/ProvisionedContainersApp/4.0')
