
server1 = repository.create(factory.configurationItem("Infrastructure/localhost_rescan", 'overthere.LocalHost', {'os': 'UNIX'}))
dict = create_random_dict({'entries':{'username':'<ignore>','email':'test@gmail.com'}})
env1 = repository.create(factory.configurationItem("Environments/local_rescan", "udm.Environment", {"members": [server1.id], "dictionaries":[dict.id]}))


application = repository.create(factory.configurationItem('Applications/PlaceHolderTestApp_rescan', 'udm.Application'))
package = repository.create(factory.configurationItem('Applications/PlaceHolderTestApp_rescan/1.0', 'udm.DeploymentPackage'))
placeholders = ["username", "email"]
file1 = createFileWithPlaceholders(package.id, "file-1", "my-file-1.txt", "Test content1", placeholders, False)

assertEquals(file1.scanPlaceholders, False)


depl = deployment.prepareInitial(package.id, env1.id)
depl = deployment.prepareAutoDeployeds(depl)


task = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(task)
deployedFileApp = repository.read('Infrastructure/localhost_rescan/file-1')
assertNotNone(deployedFileApp)

fileCiToUpdate = repository.read(file1.id)
fileCiToUpdate.scanPlaceholders = True
repository.update(fileCiToUpdate)
fileCi = repository.read(fileCiToUpdate.id)
assertEquals(fileCi.scanPlaceholders, True)


#Nothing to deploy as already deployed
depl = deployment.prepareInitial(package.id, env1.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id


task = task2.get(taskId)
rblock = task.block.blocks.get(0).block

firstBlock = task2.block(taskId, rblock.id)
assertEquals(1, len(firstBlock.steps))
assertEquals('Register deployeds', firstBlock.steps.get(0).description)

deployit.startTaskAndWait(taskId)

#Before rescan control task, isRescanned prop to be False
assertEquals(fileCi.isRescanned, False)
rescanTask = deployit.prepareControlTask(fileCi, "rescanArtifacts")
mytask = deployit.createControlTask(rescanTask)
deployit.startTask(mytask)
wait_for_task_state(mytask, TaskExecutionState.EXECUTED)
task2.archive(mytask)

rescannedFileCi = repository.read(file1.id)
assertEquals(rescannedFileCi.isRescanned, True)

#After rescan, deploying should delete and copy the artifact
depl = deployment.prepareInitial(package.id, env1.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id


task = task2.get(taskId)
rblock = task.block.blocks.get(0).block

firstBlock = task2.block(taskId, rblock.id)
assertEquals(2, len(firstBlock.steps))

assertEquals('Delete file-1 from Infrastructure/localhost_rescan', firstBlock.steps.get(0).description)
assertEquals('Copy file-1 to Infrastructure/localhost_rescan', firstBlock.steps.get(1).description)

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id).id
deployit.startTaskAndWait(undeployTask)


#tearDown
repository.delete(application.id)
repository.delete(env1.id)
repository.delete(dict.id)
repository.delete(server1.id)

