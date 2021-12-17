server = create_random_yak_server()
env = create_random_environment("env1", [server.id])
package = repository.read("Applications/DeploymentApp/1.0")

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)
assertEquals(1, len(depl.deployeds))

deployed = depl.deployeds[0]
assertEquals("yak.DeployedYakFile", deployed.type)

deployableId = deployed.deployable
deployable = repository.read(deployableId)
assertEquals("yak.YakFile", deployable.type)

containerId = deployed.container
assertEquals(server.id, containerId)

