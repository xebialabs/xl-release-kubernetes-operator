host =  repository.create(factory.configurationItem("Infrastructure/TestHost", "overthere.LocalHost", {"os": "UNIX"}))

environment = repository.create(factory.configurationItem("Environments/TestEnv", "udm.Environment", {'members': [host.id]}))

applicationCi = repository.create(factory.configurationItem('Applications/TestApp', 'udm.Application', {}))
package1 = repository.create(factory.configurationItem(applicationCi.id + "/1.0", "udm.DeploymentPackage"))
command1 = repository.create(factory.configurationItem(applicationCi.id + "/1.0/command1", "cmd.Command", {"commandLine": "sleep 1"}))

depl1 = deployment.prepareInitial(package1.id, environment.id)
depl1 = deployment.prepareAutoDeployeds(depl1)

taskId = deployment.createDeployTask(depl1).id
deployit.startTaskAndWait(taskId)

depl2 = deployment.prepareUpgrade(package1.id, depl1.deployedApplication.id)
executedDeployment = deployment.generateSelectedDeployeds([command1.id], depl2)
depl2.deployedApplication.values['forceRedeploy']='true'
taskId = deployment.createDeployTask(depl2).id

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
deployit.startTaskAndWait(taskId)


#redeploy false will should not have steps other than Register deployeds
depl3 = deployment.prepareUpgrade(package1.id, depl1.deployedApplication.id)
executedDeployment = deployment.generateSelectedDeployeds([command1.id], depl3)
depl3.deployedApplication.values['forceRedeploy']='false'
taskId = deployment.createDeployTask(depl3).id

task = task2.get(taskId)
rblock = task.block.blocks.get(0).block

firstBlock = task2.block(taskId, rblock.id)
assertEquals(1, len(firstBlock.steps))
assertEquals('Register deployeds', firstBlock.steps.get(0).description)