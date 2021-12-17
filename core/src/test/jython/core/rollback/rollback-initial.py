packageCi = importPackage('RollbackApp/1.0-rollback')
server = create_random_yak_server("yak1")
env = create_random_environment("env1", [server.id])

depl = deployment.prepareInitial(packageCi.id, env.id)
depl = deployment.generateSingleDeployed(packageCi.deployables[0], server.id, 'yak.DeployedYakCheckpointFile', depl)
assertEquals(1, len(depl.deployeds))

taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.STOPPED)

newTaskId = deployment.createRollbackTask(taskId).id

deployit.startTaskAndWait(newTaskId)
wait_for_task_state(newTaskId, TaskExecutionState.STOPPED)

deployit.startTaskAndWait(newTaskId)
wait_for_task_state(newTaskId, TaskExecutionState.DONE)

assertFalse(repository.exists(depl.deployedApplication.id))
