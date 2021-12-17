from com.xebialabs.deployit.engine.api.execution import TaskExecutionState
from com.xebialabs.deployit.engine.api.execution import StepExecutionState

env = create_random_environment_with_yak_server("env1")
yakBlockerPackage = repository.read("Applications/TaskBlockApp/1.0-blocker")

depl, taskId = deploy(yakBlockerPackage, env)

# Starting the blocking step
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTING)
wait_for_step_state(taskId, "0_1_1_1",StepExecutionState.EXECUTING)

# Aborting the blocking step
abortAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.ABORTED)

# Cancelling the blocking step
task2.cancel(taskId)
wait_for_task_state(taskId, TaskExecutionState.CANCELLED)
