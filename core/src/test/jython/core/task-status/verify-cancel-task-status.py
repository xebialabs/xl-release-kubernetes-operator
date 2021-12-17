suffix = "cancel"

server = repository.create(factory.configurationItem("Infrastructure/localhost_status" + suffix, 'overthere.LocalHost', {'os': 'UNIX'}))
env = repository.create(factory.configurationItem("Environments/local_status" + suffix, "udm.Environment", {"members": [server.id]}))

application = repository.create(factory.configurationItem('Applications/TaskStatusApp' + suffix, 'udm.Application'))
package = repository.create(factory.configurationItem(application.id + '/1.0', 'udm.DeploymentPackage'))
command1 = repository.create(factory.configurationItem(package.id + "/command1", "cmd.Command", {"commandLine": "echo hello"}))
command2 = repository.create(factory.configurationItem(package.id + "/command2", "cmd.Command", {"commandLine": "sleep 30"}))

# deploy
depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

taskId = deployment.createDeployTask(depl).id
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTING)

wait_for_task_path_status(taskId, "0_1_1_1", "DONE")
wait_for_task_path_status(taskId, "0_1_1_2", "EXECUTING")

# aborting
abortAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.ABORTED)

wait_for_task_path_status(taskId, "0_1_1_2", "FAILED")
wait_for_task_path_status(taskId, "0_1_1", "ABORTED")

# cancelling
task2.cancel(taskId)
wait_for_task_state(taskId, TaskExecutionState.CANCELLED)

# no task paths after cancelling
wait_for_task_path_status(taskId, "0_1_1_2", "")
wait_for_task_path_status(taskId, "0_1_1", "")
wait_for_task_path_status(taskId, "0_1", "")
wait_for_task_path_status(taskId, "0", "")

# tearDown
repository.delete(env.id)
repository.delete(server.id)
repository.delete(application.id)
