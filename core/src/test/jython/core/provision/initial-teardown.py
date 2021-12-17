provision = deployment.prepareInitial(pck.id, provisioning_environment.id)
provision = deployment.prepareAutoDeployeds(provision)
taskId = deployment.createDeployTask(provision).id
deployit.startTaskAndWait(taskId)

provisioned = repository.read("Infrastructure/provider/dummy1")
assertNotNone(provisioned)

teardown_task_id = deployment.createUndeployTask(provision.deployedApplication.id).id
print teardown_task_id
deployit.startTaskAndWait(teardown_task_id)
assert_not_exists("Infrastructure/provider/dummy1")
