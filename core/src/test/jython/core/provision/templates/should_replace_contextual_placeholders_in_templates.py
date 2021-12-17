provisioned_container_app_pkg = deployit.importPackage("ProvisionedContainersApp/3.0")
infra_id = 'Infrastructure/best-yakserver-placeholders_in_templates'
yak_server = repository.create(factory.configurationItem(infra_id, 'yak.YakServer', {}))
env = repository.create(
    factory.configurationItem('Environments/yakEnv-placeholders_in_templates', 'udm.Environment', {'members': [yak_server.id]}))

assertEquals(1, len(env.members))

depl = deployment.prepareInitial(provisioned_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

updatedEnv = repository.read(env.id)
assertEquals(2, len(updatedEnv.dictionaries))
sortedDict = sorted(updatedEnv.dictionaries)
assertEquals(sortedDict[0] , "Environments/dic-a")
# dic-a-2 , The first -a suffix is added when the {{%cisuffix%}} contextual placeholder is resolved from the ci if it is defined as ciname-{{%cisuffix%}}.
# the second -2 suffix is added to the ID when cardinality is > 1
assertEquals(sortedDict[1] , "Environments/dic-a-2")

dict1 = repository.read("Environments/dic-a")
assertNotNone(dict1)
# The entries in dictionary are resolved from the contextual place holder - {{%ordinal%}}.
assertEquals(dict1.entries['foo'] , "1")

dict2 = repository.read("Environments/dic-a-2")
assertNotNone(dict2)
assertEquals(dict2.entries['foo'] , "2")

provisioned1 = repository.read(infra_id + "/yakBucket-a")
assertNotNone(provisioned1)
# yakBucket-a-2 , The first -a suffix is added when the {{%cisuffix%}} contextual placeholder is resolved from the ci if it is defined as ciname-{{%cisuffix%}}.
# the second -2 suffix is added to the ID when cardinality is > 1
provisioned2 = repository.read(infra_id + "/yakBucket-a-2")
assertNotNone(provisioned2)

# clean up
repository.delete(env.id)
repository.delete(yak_server.id)
repository.delete(env.id + '/ProvisionedContainersApp')
repository.delete('Applications/ProvisionedContainersApp/3.0')
