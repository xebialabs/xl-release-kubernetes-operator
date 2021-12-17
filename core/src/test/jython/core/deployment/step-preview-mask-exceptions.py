env1 = create_random_environment_with_yak_server("env1")
env2 = create_random_environment_with_yak_server("env2")
package = repository.read("Applications/DeploymentApp/1.0")

depl = deployment.prepareInitial(package.id, env1.id)
depl = deployment.prepareAutoDeployeds(depl)

taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

depl2 = deployment.prepareInitial(package.id, env2.id)
depl2 = deployment.prepareAutoDeployeds(depl2)

assertEquals(2, len(deployment.taskPreviewBlock(depl2).blocks[0].block.steps))

deployment.validate(depl2)
