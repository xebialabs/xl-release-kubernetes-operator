### SETUP
server = create_random_yak_server('server1')
env = create_random_environment('env1', [server.id])
yakPackage2_0 = repository.read('Applications/DeploymentApp/2.0')
yakPackage4_0 = repository.read('Applications/DeploymentApp/4.0')

### TEST
depl = deployment.prepareInitial(yakPackage2_0.id, env.id)

depl = deployment.prepareAutoDeployeds(depl)
assertEquals(1, len(depl.deployeds))
task_id = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(task_id)
wait_for_task_state(task_id, TaskExecutionState.DONE)

depl2 = deployment.prepareUpgrade(yakPackage4_0.id, '%s/DeploymentApp' % env.id)
assertEquals(1, len(depl2.deployeds))
depl2 = deployment.prepareAutoDeployeds(depl2)

for d in depl2.deployeds:
    deployit.print(d)

assertEquals(2, len(depl2.deployeds))

task_id_2 = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(task_id_2)
wait_for_task_state(task_id_2, TaskExecutionState.DONE)

deployedTestYak = repository.read('%s/test.yak' % server.id)
assertNotNone(deployedTestYak)
assertEquals('%s/test.yak' % yakPackage4_0.id, deployedTestYak.deployable)

deployedYakApp = repository.read('%s/DeploymentApp' % env.id)
assertNotNone(deployedYakApp)
