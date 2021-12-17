from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

grazing_app_pkg = importPackage("GrazingApp/5.0")
blocker_app_pkg = importPackage("FailedApp/15.0")
meadow = create_random_server('meadow2', 'yak.Meadow')
yak_server = create_random_yak_server('yakserver2')
env = create_random_environment('yakEnv-failed-deployment', [meadow.id, yak_server.id])

depl = deployment.prepareInitial(blocker_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.STOPPED)
print "Task is stopped at checkpoint"

task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.FAILED)

task2.cancel(taskId)

assert_for_repo_to_be_updated("%s/GrazingApp" % env.id, 100, 1)
