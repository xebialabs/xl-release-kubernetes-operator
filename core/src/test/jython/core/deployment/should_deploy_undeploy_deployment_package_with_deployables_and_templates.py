deployed_container_app_pkg = repository.read('Applications/DeployedAppWithTemplates/1.0')
yak_server = create_random_yak_server('template-yakserver')
env = create_random_environment('yakEnv-deployables-templates', [yak_server.id])

assertEquals(1, len(env.members))

depl = deployment.prepareInitial(deployed_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

updatedEnv = repository.read(env.id)
assertEquals(1, len(updatedEnv.dictionaries))

dict1 = repository.read("Environments/yakdictionary")
assertNotNone(dict1)

assertEquals(dict1.entries['foo'], "bar")

deployed1 = repository.read("%s/yakNameSpace" % yak_server.id)
assertNotNone(deployed1)

# undeploy
taskId2 = deployment.createUndeployTask(depl.deployedApplication.id).id
deployit.startTaskAndWait(taskId2)
wait_for_task_state(taskId2, TaskExecutionState.DONE)

updatedEnv = repository.read(env.id)
assertEquals(0, len(updatedEnv.dictionaries))

assert_not_exists("Environments/yakdictionary")
assert_not_exists("%s/yakNameSpace" % yak_server.id)
