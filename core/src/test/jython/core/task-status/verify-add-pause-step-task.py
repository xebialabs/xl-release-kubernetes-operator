env = create_random_environment_with_yak_server("env1")
yakPackage4 = repository.read("Applications/TaskBlockApp/4.0")

depl, taskId = deploy(yakPackage4, env)

# Adding a pause step
task2.addPause(taskId, "0_1_1_2")

# Starting the task
deployit.startTaskAndWait(taskId)

# Should be paused
wait_for_task_state(taskId, TaskExecutionState.STOPPED)

# Verify path status
wait_for_task_path_status(taskId, "0_1_1_1", "DONE")
wait_for_task_path_status(taskId, "0_1_1_2", "PAUSED")

# Resuming the task
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

# tearDown
task2.archive(taskId)
repository.delete(env.id)
