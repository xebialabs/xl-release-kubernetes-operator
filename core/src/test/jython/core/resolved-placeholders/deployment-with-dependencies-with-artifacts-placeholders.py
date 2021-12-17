suitePrefix = 'deployed-with-placeholders-'

try:
    # Prepare infrastructure, dictionary & environment
    host1 = repository.create(factory.configurationItem('Infrastructure/%shost-1' % suitePrefix, 'overthere.LocalHost',
                                                        {'os': os_family()}))
    host2 = repository.create(factory.configurationItem('Infrastructure/%shost-2' % suitePrefix, 'overthere.LocalHost',
                                                        {'os': os_family()}))

    dict0id = 'Environments/%sDictionary-0' % suitePrefix
    dict0 = repository.create(factory.configurationItem(dict0id, 'udm.Dictionary', {'entries': {'TARGET_PATH': '/tmp'}}))

    dict1id = 'Environments/%sDictionary-1' % suitePrefix
    dict1 = repository.create(
        factory.configurationItem(dict1id, 'udm.Dictionary', {'entries': {'foo': 'FOO1', 'bar': 'BAR1'},
                                                              'restrictToContainers': [host1.id]}))

    dict2id = 'Environments/%sDictionary-2' % suitePrefix
    dict2 = repository.create(
        factory.configurationItem(dict2id, 'udm.Dictionary', {'entries': {'foo': 'FOO2', 'bar': 'BAR2'},
                                                              'restrictToContainers': [host2.id]}))

    env = repository.create(
        factory.configurationItem('Environments/%senv' % suitePrefix, 'udm.Environment',
                                  {'members': [host1.id, host2.id], 'dictionaries': [dict0.id, dict1.id, dict2.id]}))

    # Import packages
    importedPackage1 = deployit.importPackage('ResolvedPlaceholdersApplication/1.0')
    importedPackage2 = deployit.importPackage('ResolvedPlaceholdersApplicationWithDependencies/1.0')

    # Deploy application
    depl = deployment.prepareInitial(importedPackage2.id, env.id)
    depl = deployment.prepareAutoDeployeds(depl)

    taskId = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(taskId)

    # Request resolved placeholders for environment
    placeholders = placeholder.environment(env.id)

    placeholders.sort(key=lambda x: x.value)

    assertEquals(placeholders[0].key, 'TARGET_PATH')
    assertEquals(placeholders[0].value, '/tmp')
    assertEquals(placeholders[0].encrypted, False)

    assertEquals(placeholders[1].key, 'TARGET_PATH')
    assertEquals(placeholders[1].value, '/tmp')
    assertEquals(placeholders[1].encrypted, False)

    assertEquals(placeholders[2].key, 'bar')
    assertEquals(placeholders[2].value, 'BAR1')
    assertEquals(placeholders[2].encrypted, False)

    assertEquals(placeholders[3].key, 'bar')
    assertEquals(placeholders[3].value, 'BAR2')
    assertEquals(placeholders[3].encrypted, False)

    assertEquals(placeholders[4].key, 'foo')
    assertEquals(placeholders[4].value, 'FOO1')
    assertEquals(placeholders[4].encrypted, False)

    assertEquals(placeholders[5].key, 'foo')
    assertEquals(placeholders[5].value, 'FOO2')
    assertEquals(placeholders[5].encrypted, False)

    # Request resolved placeholders for host1
    placeholders = placeholder.infrastructure(host1.id)

    placeholders.sort(key=lambda x: x.value)

    assertEquals(placeholders[0].key, 'TARGET_PATH')
    assertEquals(placeholders[0].value, '/tmp')
    assertEquals(placeholders[0].encrypted, False)
    assertEquals(placeholders[0].dictionary.id, dict0id)
    assertEquals(placeholders[0].container.id, host1.id)

    assertEquals(placeholders[1].key, 'bar')
    assertEquals(placeholders[1].value, 'BAR1')
    assertEquals(placeholders[1].encrypted, False)
    assertEquals(placeholders[1].dictionary.id, dict1id)
    assertEquals(placeholders[1].container.id, host1.id)

    assertEquals(placeholders[2].key, 'foo')
    assertEquals(placeholders[2].value, 'FOO1')
    assertEquals(placeholders[2].encrypted, False)
    assertEquals(placeholders[2].dictionary.id, dict1id)
    assertEquals(placeholders[2].container.id, host1.id)

    # Request resolved placeholders for host2
    placeholders = placeholder.infrastructure(host2.id)

    placeholders.sort(key=lambda x: x.value)

    assertEquals(placeholders[0].key, 'TARGET_PATH')
    assertEquals(placeholders[0].value, '/tmp')
    assertEquals(placeholders[0].encrypted, False)
    assertEquals(placeholders[0].dictionary.id, dict0id)
    assertEquals(placeholders[0].container.id, host2.id)

    assertEquals(placeholders[1].key, 'bar')
    assertEquals(placeholders[1].value, 'BAR2')
    assertEquals(placeholders[1].encrypted, False)
    assertEquals(placeholders[1].dictionary.id, dict2id)
    assertEquals(placeholders[1].container.id, host2.id)

    assertEquals(placeholders[2].key, 'foo')
    assertEquals(placeholders[2].value, 'FOO2')
    assertEquals(placeholders[2].encrypted, False)
    assertEquals(placeholders[2].dictionary.id, dict2id)
    assertEquals(placeholders[2].container.id, host2.id)

finally:
    # Clean repository
    undeployTask1 = deployment.createUndeployTask('%s/%s' % (env.id, 'ResolvedPlaceholdersApplicationWithDependencies'))
    deployit.startTaskAndWait(undeployTask1.id)

    undeployTask2 = deployment.createUndeployTask('%s/%s' % (env.id, 'ResolvedPlaceholdersApplication'))
    deployit.startTaskAndWait(undeployTask2.id)

    repository.delete(env.id)
    repository.delete(dict0.id)
    repository.delete(dict1.id)
    repository.delete(dict2.id)
    repository.delete(host1.id)
    repository.delete(host2.id)
    repository.delete('Applications/ResolvedPlaceholdersApplicationWithDependencies')
    repository.delete('Applications/ResolvedPlaceholdersApplication')
