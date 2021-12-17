from com.xebialabs.deployit.engine.api.execution import StepExecutionState
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

grazing_app_pkg = importPackage("GrazingApp/2.0")
blocker_app_pkg = importPackage("LongRunningApp/2.0")
meadow = create_random_server('meadow-meadow', 'yak.Meadow')
yak_server = create_random_yak_server('yakserver-stopped-deployment')
env = create_random_environment('yakEnv-stopped-deployment', [meadow.id, yak_server.id])

depl = deployment.prepareInitial(blocker_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.STOPPED)
print "Task is stopped at checkopoint"

task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTING)
wait_for_step_state(taskId, "0_1_1_2_1", StepExecutionState.EXECUTING)

print "Task is started post checkpoint"

stopAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.STOPPED)

task2.cancel(taskId)
assert_for_repo_to_be_updated("%s/GrazingApp" % env.id, 100, 1)
