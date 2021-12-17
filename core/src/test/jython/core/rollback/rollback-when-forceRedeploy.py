host =  repository.create(factory.configurationItem("Infrastructure/TestHost", "overthere.LocalHost", {"os": "UNIX"}))
environment = repository.create(factory.configurationItem("Environments/TestEnv", "udm.Environment", {'members': [host.id]}))
applicationCi = repository.create(factory.configurationItem('Applications/TestApp', 'udm.Application', {}))
package1 = repository.create(factory.configurationItem(applicationCi.id + "/1.0", "udm.DeploymentPackage"))
command1 = repository.create(factory.configurationItem(applicationCi.id + "/1.0/command1", "cmd.Command", {"commandLine": "sleep 1"}))

depl1 = deployment.prepareInitial(package1.id, environment.id)
depl1 = deployment.prepareAutoDeployeds(depl1)

taskId = deployment.createDeployTask(depl1).id
assertNotNone(taskId)

deployit.startTaskAndWait(taskId)

depl2 = deployment.prepareUpgrade(package1.id, depl1.deployedApplication.id)
executedDeployment = deployment.generateSelectedDeployeds([command1.id], depl2)
depl2.deployedApplication.values['forceRedeploy']='true'

taskId = deployment.createDeployTask(depl2).id
assertNotNone(taskId)

deployit.startTask(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

task = task2.get(taskId)
rblock = task.block.blocks.get(0).block

firstBlock = task2.block(taskId, rblock.id)
assertEquals(2, len(firstBlock.steps))
assertEquals('Undo command1', firstBlock.steps.get(0).description)
assertEquals('Execute command1', firstBlock.steps.get(1).description)

lastBlock = task.block.blocks.get(1).block
lastBlockWithSteps = task2.block(taskId, lastBlock.id)
assertEquals(1, len(lastBlockWithSteps.steps))
assertEquals('Register deployeds', lastBlockWithSteps.steps.get(0).description)

taskId = deployment.createRollbackTask(taskId).id

deployit.startTask(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

task = task2.get(taskId)
rblock = task.block.blocks.get(0).block

firstBlock = task2.block(taskId, rblock.id)
assertEquals('Undo command1', firstBlock.steps.get(0).description)
assertEquals('Execute command1', firstBlock.steps.get(1).description)
task2.archive(taskId)
assertTrue(repository.exists(depl1.deployedApplication.id))

repository.delete(environment.id)
repository.delete(host.id)
repository.delete(applicationCi.id)
