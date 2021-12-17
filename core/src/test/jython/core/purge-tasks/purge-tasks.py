from test import TestUtils

def all_tasks():
    return task2.query('1/1/2000', '1/1/2050')

def get_task_ids(tasks):
    result = []
    for t in tasks:
        result.append(t.id)
    return result


## TASKS
yakServer = repository.create(factory.configurationItem('Infrastructure/yak-server', 'yak.YakServer', {}))
yakEnv = repository.create(factory.configurationItem('Environments/yak-env', 'udm.Environment', {'members': [yakServer.id]}))
ctServer = repository.create(factory.configurationItem('Infrastructure/ct-server', 'yak.StartableContainer', {'tempDir': '', 'startFileName': ''}))

startedTaskIds = []

# run control task
control = deployit.prepareControlTask(ctServer, 'start')
controlTaskId = deployit.createControlTask(control)
deployit.startTaskAndWait(controlTaskId)
startedTaskIds.append(controlTaskId)

# run deployment
packageCi = deployit.importPackage('PolicyApp/1.0-rollback')

depl = deployment.prepareInitial(packageCi.id, yakEnv.id)
depl = deployment.generateSingleDeployed(packageCi.deployables[0], yakServer.id, 'yak.DeployedYakCheckpointFile', depl)

deploymentTaskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(deploymentTaskId)
startedTaskIds.append(deploymentTaskId)

# run rollback
rollbackTaskId = deployment.createRollbackTask(deploymentTaskId).id
deployit.startTaskAndWait(rollbackTaskId)

policyCi = repository.create(factory.configurationItem('Configuration/policy-taskPolicy', 'policy.TaskRetentionPolicy',
                                                       {'taskRetention': '-1', 'dryRun': 'true', 'archivePath': 'export/tasks.zip'}))

tasks = all_tasks()
taskIds = get_task_ids(tasks)

# assert starting situation is correct
assertEquals(len(startedTaskIds), 2)
for t in startedTaskIds:
    assertTrue(t in taskIds)

try:
    # validate no tasks removed with dryRun
    deployit.executeControlTask("executeJob", policyCi)
    allTaskIdsUpdate = get_task_ids(all_tasks())
    assertTrue(len(allTaskIdsUpdate) > 2)
    for t in startedTaskIds:
        assertTrue(t in allTaskIdsUpdate)

    # disable dryRun
    policyCi.dryRun = 'false'
    policyCi = repository.update(policyCi)

    # validate tasks are removed
    deployit.executeControlTask("executeJob", policyCi)
    taskIdsAfterDryRun = get_task_ids(all_tasks())
    for t in startedTaskIds:
        assertFalse(t in taskIdsAfterDryRun)

    # validate tasks are exported

    filteredExportedTask = None
    for task in tasks:
        if task.id == deploymentTaskId:
            filteredExportedTask = task

    task_filename = "%04d/%02d/%02d/%s.xml" % (filteredExportedTask.startDate.getYear(), filteredExportedTask.startDate.getMonthOfYear(), filteredExportedTask.startDate.getDayOfMonth(), str(filteredExportedTask.id))
    content = TestUtils.readFromZip(os.path.join(_integration_server_runtime_directory, 'export/tasks.zip'), task_filename)
    assertTrue(('id="%s"' % str(filteredExportedTask.id)) in content, "Task %s was not exported" % str(filteredExportedTask.id))
    assertTrue('<log>' in content, "Task %s missing step log export. The file content is: %s" % (str(filteredExportedTask.id), content))

finally:
    repository.delete(policyCi.id)
    rmdir('export')
    task2.cancel(rollbackTaskId)
    repository.delete(yakEnv.id)
    repository.delete(yakServer.id)
    repository.delete(ctServer.id)
    repository.delete('Applications/PolicyApp')



