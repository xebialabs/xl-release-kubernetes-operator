server = create_random_yak_server()
env = create_random_environment("env1", [server.id])
package = repository.read("Applications/DeploymentApp/1.0-blocker")

deployedYakFile = factory.configurationItem('%s/test.yak' % server.id, 'yak.DeployedYakFile', {'deployable':'Applications/DeploymentApp/1.0/test.yak','container':server.id})
deployedYakFile2 = factory.configurationItem('%s/test.yak' % server.id, 'yak.DeployedYakFile', {'deployable':'Applications/DeploymentApp/1.0/test.yak','container':server.id})

depl = deployment.prepareInitial(package.id, env.id)
depl.deployeds = [deployedYakFile, deployedYakFile2]
try:
  task = deployment.createDeployTask(depl)
except:
  pass
else:
  raise Exception("Should not be validated.")
