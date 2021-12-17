from com.xebialabs.deployit.engine.api.execution import StepExecutionState

env = create_random_environment_with_yak_server("env1")
yakPackage4 = repository.read("Applications/TaskBlockApp/4.0")

depl, taskId = deploy(yakPackage4, env)

task = task2.get(taskId)

task2.skip(taskId, ["0_1_1_1", "0_1_1_2"])
assertStepState(taskId, "0_1_1_1", StepExecutionState.SKIP)
assertStepState(taskId, "0_1_1_2", StepExecutionState.SKIP)

task2.unskip(taskId, ["0_1_1_1", "0_1_1_2"])
assertStepState(taskId, "0_1_1_1", StepExecutionState.PENDING)
assertStepState(taskId, "0_1_1_2", StepExecutionState.PENDING)

task2.cancel(taskId)
