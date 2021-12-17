### SETUP
env = create_random_environment_with_yak_server("env1")
emptyPackage = repository.read('Applications/DeploymentApp3/1.0')

### TEST
depl = deployment.prepareInitial(emptyPackage.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals(0, len(depl.deployeds))
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)

wait_for_task_state(taskId, TaskExecutionState.DONE)
assertTrue(repository.exists(env.id + "/DeploymentApp3"))

