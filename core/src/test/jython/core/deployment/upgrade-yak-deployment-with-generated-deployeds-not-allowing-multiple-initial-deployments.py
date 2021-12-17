server = create_random_yak_server('server1')
env = create_random_environment('env1', [server.id])
yakPackage2_0 = repository.read('Applications/DeploymentApp/2.0')
package = repository.read("Applications/DeploymentApp/1.0")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

depl2 = deployment.prepareUpgrade(yakPackage2_0.id, '%s/DeploymentApp' % env.id)
taskId2 = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(taskId2)
wait_for_task_state(taskId2, TaskExecutionState.DONE)

deployedTestYak = repository.read('%s/test.yak' % server.id)
assertNotNone(deployedTestYak)
assertEquals('%s/test.yak' % yakPackage2_0.id, deployedTestYak.deployable)

deployedYakApp = repository.read('%s/DeploymentApp' % env.id)
assertNotNone(deployedYakApp)
