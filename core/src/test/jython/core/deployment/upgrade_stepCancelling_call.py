from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

### SETUP
server = create_random_yak_server('server1')
env = create_random_environment('env1', [server.id])
package = repository.read("Applications/DeploymentApp/1.0")
yakPackage4_0 = repository.read('Applications/DeploymentApp/4.0')
yakPackage5_0 = repository.read('Applications/DeploymentApp/5.0')

#prepare deployeds
#task1
depl1 = deployment.prepareInitial(package.id, env.id)
depl1 = deployment.prepareAutoDeployeds(depl1)
taskId = deployment.createDeployTask(depl1).id
deployit.startTaskAndWait(taskId)

#task2
depl2 = deployment.prepareUpgrade(yakPackage4_0.id, depl1.deployedApplication.id)
depl2 = deployment.prepareAutoDeployeds(depl2)
taskId2 = deployment.createDeployTask(depl2).id

task2.addPause(taskId2, "0_1_1_2")
deployit.startTaskAndWait(taskId2)
wait_for_task_state(taskId2, TaskExecutionState.STOPPED)

#task3
depl3 = deployment.prepareUpgrade(yakPackage5_0.id, depl1.deployedApplication.id)
depl3 = deployment.prepareAutoDeployeds(depl3)
taskId3 = deployment.createDeployTask(depl3).id
deployit.startTaskAndWait(taskId3)

#cancel task2
deployit.cancelTask(taskId2)
wait_for_task_state(taskId2, TaskExecutionState.CANCELLED)

assertEquals(yakPackage5_0.id, repository.read('%s/DeploymentApp' % env.id).version)
undeployTask = deployment.createUndeployTask(depl3.deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)
