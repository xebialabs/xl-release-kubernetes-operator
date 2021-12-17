provision = deployment.prepareInitial(pck.id, provisioning_environment.id)
provision = deployment.prepareAutoDeployeds(provision)

taskId = deployment.createDeployTask(provision).id

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

provisioned = repository.read("Infrastructure/provider/dummy1")
assertNotNone(provisioned)
