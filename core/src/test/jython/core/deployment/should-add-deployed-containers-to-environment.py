deployed_container_app_pkg = repository.read('Applications/DeployedContainersApp/1.0')
yak_server = create_random_yak_server('deploy-yakserver', {"tags": ['*']})
env = create_random_environment('deploy-yakEnv', [yak_server.id])

assertEquals(1, len(env.members))

depl = deployment.prepareInitial(deployed_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

updatedEnv = repository.read(env.id)
assertEquals(2, len(updatedEnv.members))

# DEPL-12695 - Should get tags from 'containerTags' instead of 'tags'
yakNameSpace = repository.read("%s/yakNameSpace" % yak_server.id)
assertEquals(1, len(yakNameSpace.tags))
assertTrue("correct" in yakNameSpace.tags)
assertFalse("wrong" in yakNameSpace.tags)

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id)

# the step in the task will do the checking because it can only be verified on the server side.
deployit.startTaskAndWait(undeployTask.id)

updatedEnv = repository.read(env.id)
assertEquals(1, len(updatedEnv.members))
