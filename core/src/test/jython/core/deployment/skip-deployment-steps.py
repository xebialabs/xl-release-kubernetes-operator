env = create_random_environment_with_yak_server("env1")
package = repository.read("Applications/DeploymentApp/1.0-blocker")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.skipSteps(taskId, [1])
deployit.startTaskAndWait(taskId)

wait_for_task_state(taskId, TaskExecutionState.DONE)
