server1 = repository.create(factory.configurationItem("Infrastructure/localhost", 'overthere.LocalHost', {'os': 'UNIX'}))
dict = create_random_dict({'entries':{'ana':'<ignore>'}, 'encryptedEntries':{'janu':'<ignore>'}})
encryptedDict = create_random_dict({'entries':{'ram':'<ignore>'}}, 'udm.EncryptedDictionary')
env1 = repository.create(factory.configurationItem("Environments/local", "udm.Environment", {"members": [server1.id], "dictionaries":[dict.id, encryptedDict.id]}))

application = repository.create(factory.configurationItem('Applications/PlaceHolderTestApp', 'udm.Application'))
package = repository.create(factory.configurationItem('Applications/PlaceHolderTestApp/1.0', 'udm.DeploymentPackage'))
placeholders = ["ana", "janu", "ram"]
file1 = createFileWithPlaceholders(package.id, "file-1", "my-file-1.txt", "Test content1", placeholders)

depl = deployment.prepareInitial(package.id, env1.id)
depl = deployment.prepareAutoDeployeds(depl)

assertNotEquals(depl.deployeds[0].placeholders['ram'],'<ignore>')
assertNotEquals(depl.deployeds[0].placeholders['janu'],'<ignore>')
assertEquals('<ignore>', depl.deployeds[0].placeholders['ana'])

if (not depl.deployeds[0].placeholders['ram'].startswith('e{{aes')):
	raise Exception("should be encrypted")
if (not depl.deployeds[0].placeholders['janu'].startswith('e{{aes')):
	raise Exception("should be encrypted")

task = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(task)
deployedFileApp = repository.read('Infrastructure/localhost/file-1')
assertNotNone(deployedFileApp)

assertNotEquals(deployedFileApp.placeholders['ram'],'<ignore>')
assertNotEquals(deployedFileApp.placeholders['janu'],'<ignore>')
assertEquals('<ignore>', deployedFileApp.placeholders['ana'])
if (not deployedFileApp.placeholders['ram'].startswith('e{{aes')):
	raise Exception("should be encrypted")
if (not deployedFileApp.placeholders['janu'].startswith('e{{aes')):
	raise Exception("should be encrypted")

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id).id
deployit.startTaskAndWait(undeployTask)

repository.delete(application.id)
repository.delete(env1.id)
repository.delete(dict.id)
repository.delete(encryptedDict.id)
repository.delete(server1.id)




