env = create_random_environment_with_yak_server("env1")
yakPackage4 = repository.read("Applications/TaskBlockApp/4.0")

depl, taskId = deploy(yakPackage4, env)

# start the task
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

# rollback
rollbackTaskId = deployment.createRollbackTask(taskId).id
task2.start(rollbackTaskId)
wait_for_task_state(rollbackTaskId, TaskExecutionState.EXECUTED)
wait_for_task_path_status(rollbackTaskId, "0_1_1_1", "DONE")
wait_for_task_path_status(rollbackTaskId, "0_1_1_2", "DONE")

# tearDown
task2.archive(rollbackTaskId)
repository.delete(env.id)
