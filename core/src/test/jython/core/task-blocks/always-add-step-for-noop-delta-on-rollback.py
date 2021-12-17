pkg_1 = importPackage("TaskBlockNoopStepContributingApp/1.0")
pkg_2 = importPackage("TaskBlockNoopStepContributingApp/2.0")
server = create_random_yak_server('task-blocks-yakserver')
env = create_random_environment('task-blocks-yakEnv', [server.id])

#Initial Deployment
depl = deployment.prepareInitial(pkg_1.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

#Update Deployment

depl = deployment.prepareUpgrade(pkg_2.id, depl.deployedApplication.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

#Rollback update
task_id2 = deployment.createRollbackTask(taskId).id

s = task2.steps(task_id2, "0_1_1")
assertEquals(3, len(s.steps))
for step in s.steps:
    print step.description

assertTrue("NoOpSpec, NOOP - Deployed State" in [s.description for s in s.steps])

# clean up
task2.cancel(task_id2)
