app = create_random_application('rollback-AppForRollback')
packageV1 = createPackage(app.id, "1.0")
v1file1 = createFile(packageV1.id, "file-1", "my-file-1.txt", "Test content")
v1file2 = createFile(packageV1.id, "file-2", "my-file-2.txt", "Test content 2")

packageV2 = createPackage(app.id, "2.0")
v2file1 = createFile(packageV2.id, "file-1", "my-file-1.txt", "Test content updated")
v2file2 = createFile(packageV2.id, "file-2", "my-file-2.txt", "Test content 2 updated")

host = createHost("rollback-localhost")
host2 = createHost("rollback-localhost2")
env = createEnvironment("rollback-local", [host, host2])

depl = deployment.prepareInitial(packageV1.id, env.id)
depl.deployedApplication.values['orchestrator'] = ['parallel-by-container']
depl = deployment.generateSingleDeployed(v1file1.id, host.id, depl)
depl = deployment.generateSingleDeployed(v1file2.id, host2.id, depl)

taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

deployit.startTask(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)
task2.archive(taskId)

# Upgrading to version 2
upgradeDepl = deployment.prepareUpgrade(packageV2.id, depl.deployedApplication.id)

upgradeTaskId = deployment.createDeployTask(upgradeDepl).id
assertNotNone(upgradeTaskId)

deployit.startTask(upgradeTaskId)
wait_for_task_state(upgradeTaskId, TaskExecutionState.EXECUTED)

rollbackTaskId = deployment.createRollbackTask(upgradeTaskId).id

deployit.startTask(rollbackTaskId)
wait_for_task_state(rollbackTaskId, TaskExecutionState.EXECUTED)
task2.archive(rollbackTaskId)

assertTrue(repository.exists(depl.deployedApplication.id))

repository.delete(env.id)
repository.delete(host.id)
repository.delete(host2.id)
repository.delete(app.id)
