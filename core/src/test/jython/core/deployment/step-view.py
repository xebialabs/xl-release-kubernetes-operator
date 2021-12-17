env = create_random_environment_with_yak_server("env1")
package = repository.read("Applications/DeploymentApp/1.0-with-requirement")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals(2, len(depl.deployeds))

steps = deployment.taskPreviewBlock(depl).blocks[0].block.steps

print(steps)

assertEquals(2, len(steps))

filter(lambda d: d.type == "yak.YakWithRequirement", depl.deployeds)[0].requirement = "Foo"

steps = deployment.taskPreviewBlock(depl).blocks[0].block.steps
print(steps)

assertEquals(3, len(steps))

deployment.validate(depl)
