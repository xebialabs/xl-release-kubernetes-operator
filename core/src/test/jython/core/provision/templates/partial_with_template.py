from xld_tasks import wait_for_task_state, start_task, archive_task, add_pause

provision = deployment.prepareInitial(provision_package_2.id, provisioning_environment.id)
provision = deployment.prepareAutoDeployeds(provision)

taskId = deployment.createDeployTask(provision).id
print taskId
add_pause(taskId, "0_1_1_1_2")
start_task(taskId)
wait_for_task_state(taskId, TaskExecutionState.STOPPED)

assert_not_exists("Infrastructure/" + template.instanceName)
assert_not_exists("Infrastructure/%s" % (template_2.name))
assert_not_exists("Infrastructure/%s-2" % (template_2.name))
assert_not_exists("Infrastructure/%s" % (template_3.name))

rollback_task_id = deployment.createRollbackTask(taskId).id
start_task(rollback_task_id)
wait_for_task_state(rollback_task_id, TaskExecutionState.EXECUTED)
archive_task(rollback_task_id)
