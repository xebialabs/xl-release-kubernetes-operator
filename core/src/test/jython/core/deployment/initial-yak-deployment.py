testServer = create_random_yak_server()
env = create_random_environment("env1", [testServer.id])
package = repository.read("Applications/DeploymentApp/1.0-blocker")

deployedYakFile = factory.configurationItem(testServer.id + '/test.yak', 'yak.DeployedYakFile', {'deployable':'Applications/DeploymentApp/1.0/test.yak','container':testServer.id})

depl = deployment.prepareInitial(package.id, env.id)
depl.deployeds = [deployedYakFile]
taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

deployedTestYak = repository.read('%s/test.yak' % testServer.id)
assertNotNone(deployedTestYak)

deployedYakApp = repository.read('%s/DeploymentApp' % env.id)
assertNotNone(deployedYakApp)

depl2 = deployment.prepareInitial(package.id, env.id)
assertEquals(Deployment.DeploymentType.UPDATE, Deployment.DeploymentType.valueOf(depl2.deploymentType))
