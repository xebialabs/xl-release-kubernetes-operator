#
# This test verifies that the references of CI's are the same for instances of the same CI's
# across the object hierarchy on the server side. This condition needs to holder over the entire request and the NodeReaderContext
# in combination with the OpenJcrSessionDuringRequestInterceptor needs to take care of this.
#

# setup
referencePackage = repository.read("Applications/IssuesApp/1.0")
referenceHost = repository.create(factory.configurationItem("Infrastructure/issues-localHost","overthere.LocalHost",{"os" : os_family() }))
referenceEnv = repository.create(factory.configurationItem("Environments/issues-referenceEnv", "udm.Environment", {"members": [referenceHost.id]}))

# deploy
depl = deployment.prepareInitial(referencePackage.id, referenceEnv.id)

depl = deployment.prepareAutoDeployeds(depl)

taskId = deployment.createDeployTask(depl).id

# the step in the task will do the checking because it can only be verified on the server side.
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

# cleanup
repository.delete(referenceEnv.id)
repository.delete(referenceHost.id)
