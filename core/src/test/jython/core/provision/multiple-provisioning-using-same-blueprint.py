def provision_task(environment_id):
    dict = create_dictionary("provisioning-dict", environment_id)
    provider1 = create_dummy_provider(name="provider1")
    provisioning_environment1 = create_provisioning_environment_with_dictionaries(name="provisioning_environment1",
                                                                                  providers=[provider1],
                                                                                  dictionaries=[dict])
    provision = deployment.prepareInitial(pck3.id, provisioning_environment1.id)
    print "provision for environment {0}".format(environment_id)
    provision = deployment.prepareAutoDeployeds(provision)
    taskId = deployment.createDeployTask(provision).id
    start_task(taskId)
    wait_for_task_state(taskId, TaskExecutionState.EXECUTED)
    assert_exists("Infrastructure/LocalHost")
    rollback(taskId)
    delete([provisioning_environment1, dict, provider1])


def rollback(task_id):
    print "Rollbacking task %s" % task_id
    rollback_task_id = deployment.createRollbackTask(task_id).id
    print rollback_task_id
    start_task(rollback_task_id)
    wait_for_task_state(rollback_task_id, TaskExecutionState.EXECUTED)
    archive_task(rollback_task_id)
    assert_not_exists("Infrastructure/LocalHost")


provision_task("provisioning-provEnv1")
provision_task("provisioning-provEnv2")
