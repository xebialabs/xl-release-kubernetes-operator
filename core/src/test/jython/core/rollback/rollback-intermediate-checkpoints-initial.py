packageCi = importPackage("RollbackApp2/1.0")
infra = create_random_server('rollback-meadow', 'yak.Meadow')
env = create_random_environment('rollback-meadow_env', [infra.id])

depl = deployment.prepareInitial(packageCi.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
task_id = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(task_id)

wait_for_task_state(task_id, TaskExecutionState.STOPPED)

deployit.startTaskAndWait(task_id)
wait_for_task_state(task_id, TaskExecutionState.STOPPED)

task_id2 = deployment.createRollbackTask(task_id).id

s = task2.steps(task_id2, "0_1_1")
assertEquals(3, len(s.steps))
for step in s.steps:
    print step.description

assertTrue("Roll me back NOOP!" in [s.description for s in s.steps])

task2.cancel(task_id2)
