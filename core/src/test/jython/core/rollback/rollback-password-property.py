packageCi = importPackage('RollbackApp/1.0-password')
server = create_random_yak_server("yak1")
env = create_random_environment("env1", [server.id])

depl = deployment.prepareInitial(packageCi.id, env.id)
depl = deployment.generateSingleDeployed(packageCi.deployables[0], server.id, 'yak.YakDeployedPasswords', depl)
assertEquals(1, len(depl.deployeds))

taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

deployit.startTask(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

rollbackTaskId = deployment.createRollbackTask(taskId).id

deployit.startTaskAndWait(rollbackTaskId)

wait_for_task_state(rollbackTaskId, TaskExecutionState.DONE)
assertFalse(repository.exists(depl.deployedApplication.id))
