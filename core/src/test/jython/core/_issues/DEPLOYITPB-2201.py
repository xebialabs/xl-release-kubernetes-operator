### SETUP
yakServer = repository.create(factory.configurationItem("Infrastructure/issues-yak1", "yak.YakServer", {}))
yakEnv = repository.create(factory.configurationItem("Environments/issues-env", "udm.Environment", {"members": [yakServer.id]}))

yakPackage2_0 = repository.read("Applications/IssuesApp3/2.0")
yakPackage4_0 = repository.read("Applications/IssuesApp3/4.0")

### TEST
depl = deployment.prepareInitial(yakPackage2_0.id, yakEnv.id)

depl = deployment.prepareAutoDeployeds(depl)
assertEquals(1, len(depl.deployeds))
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

depl2 = deployment.prepareUpgrade(yakPackage4_0.id, 'Environments/issues-env/IssuesApp3')
depl2 = deployment.generateSelectedDeployeds([yakPackage4_0.id + '/yak2.yak'], depl2)
assertEquals(2, len(depl2.deployeds))
taskId2 = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(taskId2)
wait_for_task_state(taskId2, TaskExecutionState.DONE)

repository.delete(yakPackage2_0.id)

deployedTestYak = repository.read('Infrastructure/issues-yak1/test.yak')
assertNotNone(deployedTestYak)
assertEquals('Applications/IssuesApp3/4.0/test.yak', deployedTestYak.deployable)

deployedYakApp = repository.read('Environments/issues-env/IssuesApp3')
assertNotNone(deployedYakApp)

### TEARDOWN
repository.delete(yakEnv.id)
repository.delete(yakServer.id)
