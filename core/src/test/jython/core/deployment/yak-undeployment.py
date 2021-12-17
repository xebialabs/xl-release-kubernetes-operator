server = create_random_yak_server('server1')
env = create_random_environment('env1', [server.id])
package = repository.read("Applications/DeploymentApp/1.0")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
task_id = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(task_id)
wait_for_task_state(task_id, TaskExecutionState.DONE)

task_id_2 = deployment.createUndeployTask('%s/DeploymentApp' % env.id).id
deployit.startTaskAndWait(task_id_2)
wait_for_task_state(task_id_2, TaskExecutionState.DONE)

assertFalse(repository.exists('%s/DeploymentApp' % env.id))
