from xld_tasks import wait_for_task_state, start_task, archive_task

provision = deployment.prepareInitial(provision_package_2.id, provisioning_environment_dir_path.id)

provision = deployment.prepareAutoDeployeds(provision)

taskId = deployment.createDeployTask(provision).id
start_task(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

assert_exists("Infrastructure/provisioning-test/path/%s" % template.instanceName)
assert_exists("Infrastructure/provisioning-test/path/%s" % (template_2.name))
assert_exists("Infrastructure/provisioning-test/path/%s" % (template_3.name))

rollback_task_id = deployment.createRollbackTask(taskId).id
start_task(rollback_task_id)
wait_for_task_state(rollback_task_id, TaskExecutionState.EXECUTED)
assert_not_exists("Infrastructure/provisioning-test/path/%s" % template.instanceName)
assert_not_exists("Infrastructure/provisioning-test/path/%s" % (template_2.name))
assert_not_exists("Infrastructure/provisioning-test/path/%s" % (template_3.name))

archive_task(rollback_task_id)
