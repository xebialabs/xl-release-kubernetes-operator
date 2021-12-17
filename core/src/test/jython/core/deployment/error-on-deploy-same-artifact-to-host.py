env = create_random_environment_with_yak_server("env1")
package = repository.read("Applications/DeploymentApp/1.0")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

cowApp = repository.read('Applications/DeploymentApp2/1.0')
depl2 = deployment.prepareInitial(cowApp.id, env.id)
depl2 = deployment.prepareAutoDeployeds(depl2)
try:
	taskId = deployment.createDeployTask(depl2).id
except:
	pass
else:
	raise Exception("Should not deploy same artifact twice under same name")
