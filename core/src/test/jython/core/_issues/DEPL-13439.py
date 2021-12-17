provisioned_container_app_pkg = repository.read("Applications/DeploymentAppWithProvisionables/2.0")
yak_server = repository.create(factory.configurationItem('Infrastructure/best-yakserver-DEPL-13439', 'yak.YakServer', {}))
env = repository.create(factory.configurationItem('Environments/yakEnv-DEPL-13439', 'udm.Environment', {'members': [yak_server.id]}))

depl = deployment.prepareInitial(provisioned_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

task2.addPause(taskId, "0_1_1_2_3")

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.STOPPED)

rollbackTaskId = deployment.createRollbackTask(taskId).id
deployit.startTaskAndWait(rollbackTaskId)

# DEPL-13439: Rollback fails on "Delete all provisioned configuration items" while trying to update the application with "bucket1 doesn't exist"
try:
    wait_for_task_state(rollbackTaskId, TaskExecutionState.DONE)
finally:
    repository.delete(env.id)
    repository.delete(yak_server.id)
