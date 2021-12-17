from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

env = create_random_environment_with_yak_server("env1")
package = repository.read("Applications/DeploymentApp/1.0-blocker")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
task_id = deployment.createDeployTask(depl).id
deployit.startTask(task_id)

wait_for_task_state(task_id, TaskExecutionState.EXECUTING)
tasks.abort(task_id)

wait_for_task_state(task_id, TaskExecutionState.ABORTED)

deployit.cancelTask(task_id)
wait_for_task_state(task_id, TaskExecutionState.CANCELLED)
