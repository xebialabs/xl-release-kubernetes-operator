from xld_tasks import wait_for_task_state, start_task, archive_task
provision = deployment.prepareInitial(provision_package_2.id, provisioning_environment.id)
provision = deployment.prepareAutoDeployeds(provision)

task =deployment.createDeployTask(provision).id
print task
start_task(task)
wait_for_task_state(task, TaskExecutionState.EXECUTED)
print template.instanceName
print template_2.name
assert_exists("Infrastructure/" + template.instanceName)
assert_exists("Infrastructure/%s" % (template_2.name))
assert_exists("Infrastructure/%s" % (template_3.name))

rollback_task_id = deployment.createRollbackTask(task).id
start_task(rollback_task_id)
wait_for_task_state(rollback_task_id, TaskExecutionState.EXECUTED)
assert_not_exists("Infrastructure/" + template.instanceName)
assert_not_exists("Infrastructure/%s" % (template_2.name))
assert_not_exists("Infrastructure/%s" % (template_3.name))

archive_task(rollback_task_id)
