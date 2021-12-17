env = create_random_environment_with_yak_server('env1')
yakPackage2_0 = repository.read('Applications/DeploymentApp/2.0')
package = repository.read("Applications/DeploymentApp/1.0")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
depl.deployedApplication.values['orchestrator'] = 'sequential-by-container'
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

depl2 = deployment.prepareUpgrade(yakPackage2_0.id, '%s/DeploymentApp' % env.id)
assertEquals('parallel-by-container', depl2.deployedApplication.values['orchestrator'].get(0))
