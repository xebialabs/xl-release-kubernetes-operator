suffix = "Pause"

server = repository.create(factory.configurationItem("Infrastructure/TaskStepLoglInfra" + suffix, 'overthere.LocalHost', {'os': 'UNIX'}))
env = repository.create(factory.configurationItem("Environments/TaskStepLoglEnv" + suffix, "udm.Environment", {"members": [server.id]}))

application = repository.create(factory.configurationItem('Applications/TaskStepLogApp' + suffix, 'udm.Application'))
package = repository.create(factory.configurationItem(application.id + '/1.0', 'udm.DeploymentPackage'))
command1 = repository.create(factory.configurationItem(package.id + "/command1", "cmd.Command", {"commandLine": "echo hello"}))
command2 = repository.create(factory.configurationItem(package.id + "/command2", "cmd.Command", {"commandLine": "sleep 30"}))


stepLogPkg = repository.read("Applications/TaskStepLogAppPause/1.0")

depl, taskId = deploy(stepLogPkg, env)

# Adding a pause step
task2.addPause(taskId, "0_1_1_2")

# Starting the task
deployit.startTaskAndWait(taskId)

# Should be paused
wait_for_task_state(taskId, TaskExecutionState.STOPPED)

# Verify path status
wait_for_task_path_status(taskId, "0_1_1_1", "DONE")
wait_for_task_path_status(taskId, "0_1_1_2", "PAUSED")

expected_log_0_1_1_1 = """Executing command line : 'echo hello'
hello"""
taskStepLog_0_1_1_1 = task2.getStepLog(taskId, "0_1_1_1")
assertEquals(expected_log_0_1_1_1, taskStepLog_0_1_1_1.log())

try:
    task2.getStepLog(taskId, "0_1_1_3")
except:
     pass

# Resuming the task
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

taskStepLog_0_1_1_3 = task2.getStepLog(taskId, "0_1_1_3")
expected_log_0_1_1_3 = """Executing command line : 'sleep 30'"""
assertEquals(expected_log_0_1_1_3, taskStepLog_0_1_1_3.log())

# undeploy
undeployTask = deployment.createUndeployTask(depl.deployedApplication.id).id
task2.start(undeployTask)
wait_for_task_state(undeployTask, TaskExecutionState.EXECUTED)

# archive
task2.archive(taskId)
task2.archive(undeployTask)

# no task step log after archive
try:
    taskStepLog = task2.getStepLog(taskId, "0_1_1_2")
except:
     pass
# tearDown
repository.delete(env.id)
repository.delete(server.id)
repository.delete(application.id)

