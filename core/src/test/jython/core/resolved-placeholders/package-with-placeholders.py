from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

suitePrefix = 'pkg-with-placeholders-'
deployedsAppId = 'Applications/%sDeployedsApp' % suitePrefix
dictId = 'Environments/%sDictionary' % suitePrefix
envId = 'Environments/%senv' %suitePrefix
hostId = 'Infrastructure/%sPlaceholderHost' % suitePrefix

def try_delete_ci(id):
    try:
        repository.delete(id)
    except DeployitClientException as e:
        print e.message

try:
    # Prepare applications
    deployedsApp = repository.create(factory.configurationItem(deployedsAppId, 'udm.Application'))

    # Prepare packages
    deployedsApp1_0 = repository.create(factory.configurationItem(
        deployedsAppId + '/1.0',
        'udm.DeploymentPackage',
        {'dependencyResolution': '{{resolution}}'}
    ))

    # Prepare infrastructure
    host = repository.create(factory.configurationItem(
        hostId,
        'overthere.LocalHost',
        {'os': os_family()}
    ))

    # Prepare dictionary
    dict = repository.create(factory.configurationItem(
        dictId,
        'udm.Dictionary',
        {'entries': {'resolution': 'LATEST'}}
    ))

    # Prepare environment
    env = repository.create(factory.configurationItem(
        envId,
        'udm.Environment',
        {
            'members': [hostId],
            'dictionaries': [dictId]
        }
    ))

    # Deploy application
    depl = deployment.prepareInitial(deployedsApp1_0.id, envId)
    depl = deployment.prepareAutoDeployeds(depl)

    taskId = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(taskId)

    # Request resolved placeholders for environment
    placeholders = placeholder.environment(envId)
    # Assert
    assertEquals(placeholders[0].key, 'resolution')
    assertEquals(placeholders[0].value, 'LATEST')

    # Request resolved placeholders for host
    placeholders = placeholder.infrastructure(hostId)
    # Assert
    assertEquals(len(placeholders), 0)

    #Undeploy and check for archived placeholders
    undeployTask = deployment.createUndeployTask('%s/%sDeployedsApp' % (envId, suitePrefix))
    deployit.startTaskAndWait(undeployTask.id)

    archivedPlaceholders = placeholder.archivedForEnvironmentAndTask(envId, taskId)
    assertEquals(len(archivedPlaceholders), 1)
    assertEquals(archivedPlaceholders[0].key, 'resolution')
    assertEquals(archivedPlaceholders[0].value, 'LATEST')

finally:
    # Clean repository
    repository.delete(envId)
    repository.delete(dictId)
    repository.delete(hostId)
    repository.delete(deployedsAppId)


