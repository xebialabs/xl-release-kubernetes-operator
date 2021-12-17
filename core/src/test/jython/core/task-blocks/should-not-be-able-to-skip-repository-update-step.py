from com.xebialabs.deployit.engine.api.execution import StepExecutionState

env = create_random_environment_with_yak_server("env1")
yakPackage = repository.read("Applications/TaskBlockApp/1.0")

depl, taskId = deploy(yakPackage, env)

task = task2.get(taskId)

# Trying to skip repository update step
try:
    task2.skip(taskId, ["0_2_1_1"])
except:
    pass
else:
    raise Exception('Should throw an exception that Repository Update Step cannot be skipped')

assertStepState(taskId, "0_2_1_1", StepExecutionState.PENDING)

# Trying to skip a skippable task
task2.skip(taskId, ["0_1_1_1"])
assertStepState(taskId, "0_1_1_1", StepExecutionState.SKIP)

task2.cancel(taskId)
