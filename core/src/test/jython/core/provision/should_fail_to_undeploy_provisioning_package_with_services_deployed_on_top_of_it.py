project_spec = deployit.importPackage("ProjectSpec/1.0")
project_spec_resources = deployit.importPackage("ProjectSpecResources/1.0")

cluster_server = repository.create(factory.configurationItem('Infrastructure/Cluster', 'test.Cluster', {}))
env = repository.create(factory.configurationItem('Environments/cluster-env', 'udm.Environment', {'members': [cluster_server.id]}))

assertEquals(1, len(env.members))

deplProjectSpec = deployment.prepareInitial(project_spec.id, env.id)
deplProjectSpec = deployment.prepareAutoDeployeds(deplProjectSpec)
taskIdSpec = deployment.createDeployTask(deplProjectSpec).id
deployit.startTaskAndWait(taskIdSpec)

updatedEnv = repository.read(env.id)
assertEquals(2, len(updatedEnv.members))

deplProjectSpecResources = deployment.prepareInitial(project_spec_resources.id, env.id)
deplProjectSpecResources = deployment.prepareAutoDeployeds(deplProjectSpecResources)
taskIdResources = deployment.createDeployTask(deplProjectSpecResources).id
deployit.startTaskAndWait(taskIdResources)

# undeploy of ProvisioningPackage before resources that are deployed on top of it should fail with com.xebialabs.deployit.repository.ItemInUseException
try:
    undeployTask = deployment.createUndeployTask(deplProjectSpec.deployedApplication.id)
except:
    pass
else:
    raise Exception('It should throw ItemInUseException exception')

# clean up
repository.delete(env.id + '/ProjectSpecResources')
repository.delete(env.id + '/ProjectSpec')
repository.delete(env.id)
repository.delete(cluster_server.id)
repository.delete('Applications/ProjectSpec')
repository.delete('Applications/ProjectSpecResources')