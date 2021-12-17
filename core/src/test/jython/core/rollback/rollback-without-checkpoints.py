app = create_random_application('rollback-AppForRollbackDemo')
packageV1 = createPackage(app.id, "1.0")

packageV2 = createPackage(app.id, "2.0")

host = createHost("rollback-local-demo-host")
env = createEnvironment("rollback-local-demo", [host])

depl = deployment.prepareInitial(packageV1.id, env.id)
demo1 = repository.create(factory.configurationItem(concat_id(packageV1.id, "Demo1.0") , "demo.DemoDeployable", {'DemoProperty' : 'demo1'}))
depl = deployment.generateSingleDeployed(demo1.id, host.id, depl)

taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

deployit.startTask(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)
task2.archive(taskId)

# Upgrading to version 2
upgradeDepl = deployment.prepareUpgrade(packageV2.id, depl.deployedApplication.id)
demo2 = repository.create(factory.configurationItem(concat_id(packageV2.id, "Demo2.0") , "demo.DemoDeployable", {'DemoProperty' : 'demo2'}))
upgradeDepl = deployment.generateSingleDeployed(demo2.id, host.id, upgradeDepl)

upgradeTaskId = deployment.createDeployTask(upgradeDepl).id
assertNotNone(upgradeTaskId)

deployit.startTask(upgradeTaskId)
wait_for_task_state(upgradeTaskId, TaskExecutionState.EXECUTED)

rollbackTaskId = deployment.createRollbackTask(upgradeTaskId).id

deployit.startTask(rollbackTaskId)
wait_for_task_state(rollbackTaskId, TaskExecutionState.EXECUTED)
task2.archive(rollbackTaskId)

assertTrue(repository.exists(depl.deployedApplication.id))

repository.delete(env.id)
repository.delete(host.id)
repository.delete(app.id)
