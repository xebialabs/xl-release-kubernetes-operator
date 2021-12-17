from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException
from java.io import File

suitePrefix = 'embedded-deployeds-with-placeholders-'
hostId = 'Infrastructure/%shost' % suitePrefix
yakServerId = 'Infrastructure/%syakServer' % suitePrefix
dictId = 'Environments/%sDictionary' % suitePrefix
yakEnvId = 'Environments/%syakEnv' % suitePrefix
importedPackageId = 'EmbeddedArtifactsWithPlaceholders/3.0'
appId = 'Applications/%s' % importedPackageId
file1 = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployed-1.yak")
file2 = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployed-2.yak")

def try_delete_ci(id):
    try:
        repository.delete(id)
    except DeployitClientException as e:
        print e.message

def try_undeploy(envId):
    try:
        undeployTask = deployment.createUndeployTask('%s/EmbeddedArtifactsWithPlaceholders' % envId)
        deployit.startTaskAndWait(undeployTask.id)
    except DeployitClientException as e:
        print e.message

try:
    # Import package
    importedPackage = deployit.importPackage(importedPackageId)

    embArtFile1 = repository.read(importedPackage.id + '/nested/file1')
    embArtFile1 = repository.rename(embArtFile1, '{{embeddedName}}-file1')

    embArtFile2 = repository.read(importedPackage.id + '/nested/file2')
    embArtFile2 = repository.rename(embArtFile2, '{{embeddedName}}-file2')

    parent = repository.read(importedPackage.id + '/nested')
    parent = repository.rename(parent, '{{parentName}}-nested')

    # Prepare infrastructure
    host = repository.create(factory.configurationItem(hostId, 'overthere.LocalHost', {'os': os_family()}))
    yakServer = repository.create(factory.configurationItem(yakServerId, 'yak.YakServer', {'host': host.id}))

    # Prepare dictionary
    dict = repository.create(factory.configurationItem(
        dictId,
        'udm.Dictionary',
        {'entries': {
            'parentName': 'parent',
            'embeddedName': 'artifact'
        }}
    ))

    # Prepare environment
    yakEnv = repository.create(factory.configurationItem(yakEnvId, 'udm.Environment', {
        'members': [yakServerId],
        'dictionaries': [dictId]
    }))

    # Deploy application
    depl = deployment.prepareInitial(appId, yakEnvId)
    depl = deployment.prepareAutoDeployeds(depl)

    assertNotNone(depl.deployeds)
    assertEquals(3, len(depl.deployeds))

    depl.deployeds[1].tempFile = file1.path
    depl.deployeds[2].tempFile = file2.path

    taskId = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(taskId)

    # Request resolved placeholders for environment
    placeholders = placeholder.environment(yakEnvId)

    # Key-Value pairs from the same deployed application have different order depending on db
    if placeholders[0].key == 'parentName':
        assertEquals(placeholders[0].key, 'parentName')
        assertEquals(placeholders[0].value, 'parent')
    else:
        assertEquals(placeholders[0].key, 'embeddedName')
        assertEquals(placeholders[0].value, 'artifact')

    if placeholders[1].key == 'parentName':
        assertEquals(placeholders[1].key, 'parentName')
        assertEquals(placeholders[1].value, 'parent')
    else:
        assertEquals(placeholders[1].key, 'embeddedName')
        assertEquals(placeholders[1].value, 'artifact')

finally:
    # Clean repository
    file1.delete()
    file2.delete()

    try_undeploy(yakEnvId)

    try_delete_ci(yakEnvId)
    try_delete_ci(dictId)
    try_delete_ci(yakServerId)
    try_delete_ci(hostId)
    try_delete_ci(appId)
