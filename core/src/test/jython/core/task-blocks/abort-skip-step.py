from com.xebialabs.deployit.engine.api.execution import TaskExecutionState
from com.xebialabs.deployit.engine.api.execution import StepExecutionState

env = create_random_environment_with_yak_server("rules-RetryStepEnv")
yakBlockerPackage = repository.read("Applications/TaskBlockApp/1.0-blocker")

depl, taskId = deploy(yakBlockerPackage, env)

# Starting the  task
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTING)
wait_for_step_state(taskId, "0_1_1_1",StepExecutionState.EXECUTING)

# Aborting the custom  step added via rule itest.customRETRY_STEP
abortAndWait(taskId)
wait_for_step_state(taskId, "0_1_1_1",StepExecutionState.FAILED)
wait_for_task_state(taskId, TaskExecutionState.ABORTED)

# Skipping the aborted step
task2.skip(taskId, ["0_1_1_1"])
assertStepState(taskId, "0_1_1_1", StepExecutionState.SKIP)

#continue
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)
