suitePrefix = 'deployed-with-placeholders-'

try:
    # Prepare infrastructure, dictionary & environment
    host = repository.create(factory.configurationItem('Infrastructure/%shost' % suitePrefix, 'overthere.LocalHost',
                                                       {'os': os_family()}))
    dict = repository.create(factory.configurationItem('Environments/%sDictionary' % suitePrefix, 'udm.Dictionary',
                                                       {'entries': {'foo': 'FOO', 'bar': 'BAR'}}))
    env = repository.create(factory.configurationItem('Environments/%senv' % suitePrefix, 'udm.Environment',
                                                      {'members': [host.id], 'dictionaries': [dict.id]}))

    # Import package
    importedPackage = deployit.importPackage('PlaceholderArtifactApp/1.0')

    # Deploy application
    depl = deployment.prepareInitial(importedPackage.id, env.id)
    depl = deployment.prepareAutoDeployeds(depl)

    taskId = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(taskId)

    # Request resolved placeholders for environment
    placeholders = placeholder.environment(env.id)

    assertEquals(placeholders[0].key, 'foo')
    assertEquals(placeholders[0].value, 'FOO')
    assertEquals(placeholders[0].encrypted, False)

    # Request resolved placeholders for host
    placeholders = placeholder.infrastructure(host.id)

    assertEquals(placeholders[0].key, 'foo')
    assertEquals(placeholders[0].value, 'FOO')
    assertEquals(placeholders[0].encrypted, False)
finally:
    # Clean repository
    undeployTask = deployment.createUndeployTask('%s/%s' % (env.id, 'PlaceholderArtifactApp'))
    deployit.startTaskAndWait(undeployTask.id)
    repository.delete(env.id)
    repository.delete(dict.id)
    repository.delete(host.id)
    repository.delete('Applications/PlaceholderArtifactApp')
