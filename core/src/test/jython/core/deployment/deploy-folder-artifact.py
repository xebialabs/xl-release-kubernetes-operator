### SETUP
env = create_random_environment_with_yak_server("env1")
yakPackage5_0 = repository.read('Applications/DeploymentApp/5.0')

### TEST
depl = deployment.prepareInitial(yakPackage5_0.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals(1, len(depl.deployeds))
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)
