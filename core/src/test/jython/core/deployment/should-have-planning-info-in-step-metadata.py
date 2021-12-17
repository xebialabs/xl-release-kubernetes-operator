env = create_random_environment_with_yak_server("env1")
package = repository.read("Applications/DeploymentApp/1.0-blocker")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

taskWithSteps = tasks.steps(taskId)
assertEquals(2, len(taskWithSteps.steps))
assertEquals(depl.deployeds[0].id, taskWithSteps.getStep(1).metadata["deployed_0"])
assertEquals("yak.DeployedYakBlocker.create_CREATE", taskWithSteps.getStep(1).metadata["rule"])
assertEquals("40", taskWithSteps.getStep(1).metadata["order"])
assertEquals("false", taskWithSteps.getStep(1).metadata["previewAvailable"])

task2.cancel(taskId)
