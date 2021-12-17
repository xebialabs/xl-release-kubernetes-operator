def all_tasks():
    return task2.getAllCurrentTaskSummaries()

def get_task_ids(tasks):
    result = []
    for t in tasks:
        result.append(t.id)
    return result

policyCi = repository.create(factory.configurationItem('Configuration/policy-taskPolicy', 'policy.TaskArchivePolicy',
                                                       {'taskRetention': '0', 'dryRun': 'true'}))

yakServer = repository.create(factory.configurationItem('Infrastructure/policy-yak-server', 'yak.YakServer', {}))
yakEnv = repository.create(factory.configurationItem('Environments/policy-yak-env', 'udm.Environment', {'members': [yakServer.id]}))

packageCi = deployit.importPackage('PolicyApp/1.0-rollback')

executedDeployment = deployment.prepareInitial(packageCi.id, yakEnv.id)
executedDeployment = deployment.generateSingleDeployed(packageCi.deployables[0], yakServer.id, 'yak.DeployedYakCheckpointFile', executedDeployment)
executedTaskId = deployment.createDeployTask(executedDeployment).id
task2.start(executedTaskId)
wait_for_task_state(executedTaskId, TaskExecutionState.STOPPED)
task2.start(executedTaskId)
wait_for_task_state(executedTaskId, TaskExecutionState.EXECUTED)

failedYak = deployit.importPackage('PolicyApp2/13.0')
failedDepl = deployment.prepareInitial(failedYak.id, yakEnv.id)
failedDepl = deployment.generateSingleDeployed(failedYak.deployables[0], yakServer.id, 'yak.DeployedYakFail', failedDepl)
failedTaskId = deployment.createDeployTask(failedDepl).id
task2.start(failedTaskId)
wait_for_task_state(failedTaskId, TaskExecutionState.FAILED)

try:
    taskIds = get_task_ids(all_tasks())
    #tasks = all_tasks()
    assertTrue(executedTaskId in taskIds)
    assertTrue(failedTaskId in taskIds)

    # now exucute dry run
    deployit.executeControlTask("executeJob", policyCi)
    # tasks should still be there

    taskIds2 = get_task_ids(all_tasks())
    assertTrue(executedTaskId in taskIds2)
    assertTrue(failedTaskId in taskIds2)

    # now run for real
    policyCi.dryRun = 'false'
    policyCi = repository.update(policyCi)

    deployit.executeControlTask("executeJob", policyCi)

    # tasks should be gone now
    taskIds3 = get_task_ids(all_tasks())
    assertFalse(executedTaskId in taskIds3)
    assertFalse(failedTaskId in taskIds3)

finally:
    repository.delete(policyCi.id)
    repository.delete(yakEnv.id)
    repository.delete(yakServer.id)
    repository.delete('Applications/PolicyApp')
    repository.delete('Applications/PolicyApp2')

    # Archive tasks
    if task2.get(executedTaskId).state is TaskExecutionState.EXECUTED:
        task2.archive(executedTaskId)
        rollbackId = deployment.createRollbackTask(executedTaskId).id
        deployit.startTaskAndWait(rollbackId)

    if task2.get(failedTaskId).state is TaskExecutionState.FAILED:
        task2.cancel(failedTaskId)



