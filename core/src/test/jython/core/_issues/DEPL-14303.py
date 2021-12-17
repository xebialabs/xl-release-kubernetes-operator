hosts = list(map(lambda i: "Infrastructure/issue-14303-host{:03}".format(i), range(1, 101)))
try:
    for h in hosts: repository.create(factory.configurationItem(h, "yak.YakServer", {}))
    env = repository.create(
        factory.configurationItem('Environments/issue-14303-env', 'udm.Environment', {'members': hosts}))

    app = createApp('issue-14303-app')
    packagev1 = createPackage(app.id, '1.0.0')
    packagev2 = createPackage(app.id, '2.0.0')

    repository.create(factory.configurationItem(packagev1.id + "/config1-00", 'yak.YakConfigurationSpec', {}))
    repository.create(factory.configurationItem(packagev2.id + "/config2-00", 'yak.YakConfigurationSpec', {}))
    for i in range(1, 11):
        repository.create(
            factory.configurationItem(packagev1.id + "/config-shared-{:02}".format(i), 'yak.YakConfigurationSpec', {}))
        repository.create(
            factory.configurationItem(packagev2.id + "/config-shared-{:02}".format(i), 'yak.YakConfigurationSpec', {}))

    depl = deployment.prepareInitial(packagev1.id, env.id)
    depl = deployment.prepareAutoDeployeds(depl)
    taskIdInitial = deployment.createDeployTask(depl).id
    assertNotNone(taskIdInitial)

    # This line is added for debugging this flaky test case as part of https://digitalai.atlassian.net/browse/ENG-2770
    # The assertion error will be catched and the real reason why it fails will be revealed
    try:
        deployit.startTaskAndWait(taskIdInitial)
        wait_for_task_state(taskIdInitial, TaskExecutionState.DONE)
    except AssertionError as ae:
        print(ae)

    depl2 = deployment.prepareUpgrade(packagev2.id, env.id + '/issue-14303-app')
    depl2 = deployment.prepareAutoDeployeds(depl2)
    taskIdUpdate = deployment.createDeployTask(depl2).id
    deployit.startTaskAndWait(taskIdUpdate)
    wait_for_task_state(taskIdInitial, TaskExecutionState.DONE)
finally:
    repository.delete('Environments/issue-14303-env')
    repository.deleteList(hosts)
    repository.delete('Applications/issue-14303-app')
