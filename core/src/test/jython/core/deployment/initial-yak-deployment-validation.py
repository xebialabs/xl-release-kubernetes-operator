server = create_random_yak_server()
env = create_random_environment("env1", [server.id])

package = repository.read('Applications/DeploymentApp/3.0')
deployedYakFile = factory.configurationItem(server.id + '/placeholders.txt', 'yak.DeployedYakPlaceholders', {'deployable':'Applications/DeploymentApp/3.0/placeholders.txt','container':server.id})

depl = deployment.prepareInitial(package.id, env.id)
depl.deployeds = [deployedYakFile]
depl = deployment.validate(depl)

assertEquals(3, len(depl.deployeds[0].validations))
