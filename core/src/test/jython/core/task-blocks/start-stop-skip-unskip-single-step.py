from com.xebialabs.deployit.engine.api.execution import StepExecutionState
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

server = create_random_dummy_server()
env = create_random_environment("env1", [server.id])
dummyPackage = repository.read("Applications/TaskBlockApp2/1.0")

depl, taskId = deploy(dummyPackage, env)

task = task2.get(taskId)

task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTING)

stopAndWait(taskId)
assertStepState(taskId, "0_1_1_1", StepExecutionState.DONE)
assertStepState(taskId, "0_1_1_9", StepExecutionState.PENDING)

# Skipping task 9"
task2.skip(taskId, ["0_1_1_9"])
assertStepState(taskId, "0_1_1_9", StepExecutionState.SKIP)

# Un-skipping task 9"
task2.unskip(taskId, ["0_1_1_9"])
assertStepState(taskId, "0_1_1_9", StepExecutionState.PENDING)

task2.cancel(taskId)
