from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

# prepare data
shopFrontendApp1 = create_random_application("app-dependencies-ShopFrontend")
shopBackendApp1 = create_random_application("app-dependencies-ShopBackend")
shopServicesApp1 = create_random_application('app-dependencies-ShopServices')
env = create_random_environment_with_yak_server("env1")

shopFrontendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopFrontendApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopBackendApp1.name: "2.0"}}))
shopBackendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopBackendApp1.id, 'udm.DeploymentPackage', {}))
shopBackendPackage_2_0 = repository.create(factory.configurationItem('%s/2.0' % shopBackendApp1.id, 'udm.DeploymentPackage', {}))

backendDeployable_1 = repository.create(factory.configurationItem('%s/backendDeployable' % shopBackendPackage_1_0.id, 'yak.YakConfigurationSpec', {}))
backendDeployable_2 = repository.create(factory.configurationItem('%s/backendDeployable' % shopBackendPackage_2_0.id, 'yak.YakConfigurationSpec', {}))
backendDeployable_2_additional = repository.create(factory.configurationItem('%s/backendDeployableAdditional' % shopBackendPackage_2_0.id, 'yak.YakConfigurationSpec', {}))
frontendDeployable = repository.create(factory.configurationItem('%s/frontendDeployable' % shopFrontendPackage_1_0.id, 'yak.YakConfigurationSpec', {}))

# deploy shopFrontendPackage_1_0
depl_1 = deployment.prepareInitial(shopFrontendPackage_1_0.id, env.id)
depl_1 = deployment.prepareAutoDeployeds(depl_1)
deployment.validate(depl_1)
taskid = deployment.createDeployTask(depl_1).id
deployit.startTaskAndWait(taskid)

# try to downgrade

try:
    depl = deployment.prepareUpgrade(shopBackendPackage_1_0.id, depl_1.requiredDeployments[0].deployedApplication.id)
except DeployitClientException, ex:
    assertTrue("Application \"%s\" cannot be upgraded, because the deployed application \"%s\" depends on its current version. It requires a version compatible with '2.0'." % (shopBackendApp1.id, shopFrontendApp1.id) in ex.message, "The exception message doesn't signal that the frontend depends on the backend, instead it says:" + ex.message)
else:
    fail("A Runtime exception should have been thrown due to broken dependency")

#cleaning up

undeployTask = deployment.createUndeployTask(depl_1.deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

undeployTask = deployment.createUndeployTask(depl_1.requiredDeployments[0].deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

# check undeployment is succesfull
assertEquals(False, repository.exists(depl_1.deployedApplication.id))
assertEquals(False, repository.exists(depl_1.deployedApplication.id))
assertEquals(False, repository.exists(depl_1.requiredDeployments[0].deployedApplication.id))
