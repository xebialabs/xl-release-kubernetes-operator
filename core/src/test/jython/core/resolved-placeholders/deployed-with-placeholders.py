from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException
from java.io import File

suitePrefix = 'deployed-with-placeholders-'
hostId = 'Infrastructure/%shost' % suitePrefix
dictId = 'Environments/%sDictionary' % suitePrefix
envId = 'Environments/%senv' % suitePrefix

def try_delete_ci(id):
    try:
        repository.delete(id)
    except DeployitClientException as e:
        print e.message

try:
    # Import package
    importedPackage = deployit.importPackage('FileApp/2.0')
    fileCi = repository.read(importedPackage.id + '/file1.txt')
    fileCi.targetFileName = '{{target}}'
    fileCi = repository.update(fileCi)

    # Prepare infrastructure
    host = repository.create(factory.configurationItem(hostId, 'overthere.LocalHost', {'os': os_family()}))

    # Prepare dictionary
    dict = repository.create(factory.configurationItem(
        dictId,
        'udm.Dictionary',
        {'entries':{'target':'test'}}
    ))

    # Prepare environment
    env = repository.create(factory.configurationItem(envId, 'udm.Environment', {
        'members': [hostId],
        'dictionaries': [dictId]
    }))

    # Deploy application
    depl = deployment.prepareInitial(importedPackage.id, envId)
    depl = deployment.prepareAutoDeployeds(depl)

    file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "file1.txt")

    taskId = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(taskId)

    # Request resolved placeholders for environment
    placeholders = placeholder.environment(envId)

    assertEquals(placeholders[0].key, 'target')
    assertEquals(placeholders[0].value, 'test')
    assertEquals(placeholders[0].encrypted, False)

    # Request resolved placeholders for host
    placeholders = placeholder.infrastructure(hostId)

    assertEquals(placeholders[0].key, 'target')
    assertEquals(placeholders[0].value, 'test')
    assertEquals(placeholders[0].encrypted, False)

finally:
    # Clean repository
    undeployTask = deployment.createUndeployTask('%s/%s' % (envId, 'FileApp'))
    deployit.startTaskAndWait(undeployTask.id)
    try_delete_ci(envId)
    try_delete_ci(dictId)
    try_delete_ci(hostId)
    try_delete_ci('Applications/FileApp')

