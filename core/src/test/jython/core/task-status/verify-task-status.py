server = repository.create(factory.configurationItem("Infrastructure/localhost_status", 'overthere.LocalHost', {'os': 'UNIX'}))
env = repository.create(factory.configurationItem("Environments/local_status", "udm.Environment", {"members": [server.id]}))


application = repository.create(factory.configurationItem('Applications/TaskStatusApp', 'udm.Application'))
package = repository.create(factory.configurationItem('Applications/TaskStatusApp/1.0', 'udm.DeploymentPackage'))
file1 = createFile(package.id, "file-task-status", "task-status.txt", "Task Status")

# deploy
depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

task = deployment.createDeployTask(depl).id
task2.start(task)
wait_for_task_state(task, TaskExecutionState.EXECUTED)

wait_for_task_path_status(task, "0_1_1_1", "DONE")

# undeploy
undeployTask = deployment.createUndeployTask(depl.deployedApplication.id).id
task2.start(undeployTask)
wait_for_task_state(undeployTask, TaskExecutionState.EXECUTED)

wait_for_task_path_status(undeployTask, "0_1_1_1", "DONE")

# tearDown
task2.archive(task)
task2.archive(undeployTask)
repository.delete(application.id)
repository.delete(env.id)
repository.delete(server.id)

