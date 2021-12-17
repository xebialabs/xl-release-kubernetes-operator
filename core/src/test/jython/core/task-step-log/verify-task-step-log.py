server = repository.create(factory.configurationItem("Infrastructure/TaskStepLogInfra", 'overthere.LocalHost', {'os': 'UNIX'}))
env = repository.create(factory.configurationItem("Environments/TaskStepLogEnv", "udm.Environment", {"members": [server.id]}))


application = repository.create(factory.configurationItem('Applications/TaskStepLogApp', 'udm.Application'))
package = repository.create(factory.configurationItem('Applications/TaskStepLogApp/1.0', 'udm.DeploymentPackage'))
deployableCis = repository.create(factory.configurationItem(package.id + '/TaskStepLogCommand', 'cmd.Command', {'commandLine': 'echo hello world'}))

# deploy
depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

task = deployment.createDeployTask(depl).id
task2.start(task)
wait_for_task_state(task, TaskExecutionState.EXECUTED)

wait_for_task_path_status(task, "0_1_1_1", "DONE")

expected_log = """Executing command line : 'echo hello world'
hello world"""
taskStepLog = task2.getStepLog(task, "0_1_1_1")
print(expected_log==taskStepLog.log())
assertEquals(taskStepLog.log(), expected_log)


# undeploy
undeployTask = deployment.createUndeployTask(depl.deployedApplication.id).id
task2.start(undeployTask)
wait_for_task_state(undeployTask, TaskExecutionState.EXECUTED)

# archive
task2.archive(task)
task2.archive(undeployTask)

# no task step log after archive
try:
    taskStepLog = task2.getStepLog(taskId, "0_1_1_2")
except:
     pass

# tearDown
repository.delete(application.id)
repository.delete(env.id)
repository.delete(server.id)

