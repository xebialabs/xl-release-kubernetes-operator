suffix = "Cancel"

server = repository.create(factory.configurationItem("Infrastructure/TaskStepLoglInfra" + suffix, 'overthere.LocalHost', {'os': 'UNIX'}))
env = repository.create(factory.configurationItem("Environments/TaskStepLoglEnv" + suffix, "udm.Environment", {"members": [server.id]}))

application = repository.create(factory.configurationItem('Applications/TaskStepLogApp' + suffix, 'udm.Application'))
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

expected_log_0_1_1_2 = """Executing command line : 'sleep 30'
Execution interrupted"""
taskStepLog = task2.getStepLog(taskId, "0_1_1_2")
print(expected_log_0_1_1_2==taskStepLog.log()) 
print(taskStepLog.log)
assertEquals(taskStepLog.log(), expected_log_0_1_1_2)

# cancelling
task2.cancel(taskId)
wait_for_task_state(taskId, TaskExecutionState.CANCELLED)

# no task step log after cancelling
try:
    taskStepLog = task2.getStepLog(taskId, "0_1_1_2")    
except:
     pass

# tearDown
repository.delete(env.id)
repository.delete(server.id)
repository.delete(application.id)

