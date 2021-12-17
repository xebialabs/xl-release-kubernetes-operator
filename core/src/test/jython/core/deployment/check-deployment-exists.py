env = create_random_environment_with_yak_server("env1")
package = repository.read("Applications/DeploymentApp/1.0")

assertFalse(deployment.isDeployed(package.application, env.id))

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
task_id = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(task_id)

wait_for_task_state(task_id, TaskExecutionState.DONE)
assertTrue(deployment.isDeployed(package.application, env.id))
