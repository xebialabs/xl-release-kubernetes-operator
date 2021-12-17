server = create_random_yak_server()
env = create_random_environment("env1", [server.id])
package = repository.read("Applications/DeploymentApp/1.0")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

deployedTestYak = repository.read('%s/test.yak' % server.id)
assertNotNone(deployedTestYak)

deployedYakApp = repository.read('%s/DeploymentApp' % env.id)
assertNotNone(deployedYakApp)
