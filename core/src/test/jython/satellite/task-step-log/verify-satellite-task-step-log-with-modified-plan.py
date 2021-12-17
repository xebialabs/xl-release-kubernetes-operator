application = repository.create(factory.configurationItem('Applications/Satellite-Cmd-App', 'udm.Application'))
package = repository.create(factory.configurationItem(application.id + '/1.0', 'udm.DeploymentPackage'))
command = repository.create(factory.configurationItem(package.id + "/command", "cmd.Command", {"commandLine": "echo hello"}))

# deploy
depl = deployment.prepareInitial(package.id, 'Environments/satellite-env')
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

try:
    # Adding a pause step
    task2.addPause(taskId, "0_2_1_1")
    task2.start(taskId)
    wait_for_task_state(taskId, TaskExecutionState.STOPPED)

    # Adding a pause step for an active task
    task2.addPause(taskId, "0_2_1_2")
    task2.start(taskId)
    wait_for_task_state(taskId, TaskExecutionState.STOPPED)
    task2.start(taskId)
    wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

    # Verify step log
    taskStepLog = task2.getStepLog(taskId, "0_2_1_3")
    assertNotNone(taskStepLog.log())
finally:
    # undeploy
    undeployTaskId = deployment.createUndeployTask(depl.deployedApplication.id).id
    task2.start(undeployTaskId)
    wait_for_task_state(undeployTaskId, TaskExecutionState.EXECUTED)

    # tearDown
    repository.delete(application.id)
