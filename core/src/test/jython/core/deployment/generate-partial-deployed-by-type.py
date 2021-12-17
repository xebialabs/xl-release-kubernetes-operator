server = create_random_yak_server()
env = create_random_environment("env1", [server.id])
package = repository.read("Applications/DeploymentApp/1.0-restart")

depl = deployment.prepareInitial(package.id, env.id)
deployeds = deployment.generateSingleDeployed('%s/test.yak' % package.id, server.id, 'yak.RestartRequiringDeployedYakFile', depl).deployeds

assertEquals(1, len(deployeds))
assertEquals('yak.RestartRequiringDeployedYakFile', deployeds[0].type)
assertEquals('%s/test.yak' % package.id, deployeds[0].deployable)
assertEquals(server.id, deployeds[0].container)
