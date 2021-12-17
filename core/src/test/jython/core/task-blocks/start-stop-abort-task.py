from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

env = create_random_environment_with_yak_server("env1")
yakBlockerPackage = repository.read("Applications/TaskBlockApp/1.0-blocker")

# Deploying a package with blocking step
depl, taskId = deploy(yakBlockerPackage, env)

# Starting the blocking step
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTING)

# Stopping the blocking step
task2.stop(taskId)
wait_for_task_state(taskId, TaskExecutionState.STOPPING)

# Aborting the stopping step
abortAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.ABORTED)

# Cancelling the blocking step
task2.cancel(taskId)
wait_for_task_state(taskId, TaskExecutionState.CANCELLED)
