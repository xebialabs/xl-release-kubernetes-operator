def performProvisioning(pckId):
    provision = deployment.prepareInitial(pckId, provisioning_environment.id)
    provision = deployment.prepareAutoDeployeds(provision)
    taskId = deployment.createDeployTask(provision).id
    deployit.startTaskAndWait(taskId)
    wait_for_task_state(taskId, TaskExecutionState.DONE)
    provisioned = repository.read("Infrastructure/provider/dummy1")
    assertNotNone(provisioned)


# First deployment with provisioning package
performProvisioning(pck.id)

# Second deployment with another provisioning package with same provisionable name
#performProvisioning(pck_copy.id)
