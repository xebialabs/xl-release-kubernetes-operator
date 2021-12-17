# prepare data
testSalt = UUID.randomUUID().toString()

shopFrontendApp1 = create_random_application("app-dependencies-ShopFrontend", {}, testSalt)
shopBackendApp1 = create_random_application("app-dependencies-ShopBackend", {}, testSalt)
shopServicesApp1 = create_random_application('app-dependencies-ShopServices', {}, testSalt)
env = create_random_environment_with_yak_server("env1")

shopFrontendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopFrontendApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopBackendApp1.name: "[1.0, 2.0]"}}))
shopBackendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopBackendApp1.id, 'udm.DeploymentPackage', {}))
shopBackendPackage_2_0 = repository.create(factory.configurationItem('%s/2.0' % shopBackendApp1.id, 'udm.DeploymentPackage', {}))

backendDeployable_1 = repository.create(factory.configurationItem('%s/backendDeployable' % shopBackendPackage_1_0.id, 'yak.YakConfigurationSpec', {}))
backendDeployable_2 = repository.create(factory.configurationItem('%s/backendDeployable' % shopBackendPackage_2_0.id, 'yak.YakConfigurationSpec', {}))
backendDeployable_2_additional = repository.create(factory.configurationItem('%s/backendDeployableAdditional' % shopBackendPackage_2_0.id, 'yak.YakConfigurationSpec', {}))
frontendDeployable = repository.create(factory.configurationItem('%s/frontendDeployable' % shopFrontendPackage_1_0.id, 'yak.YakConfigurationSpec', {}))

# deploy shopBackendPackage_1_0
depl_1 = deployment.prepareInitial(shopBackendPackage_1_0.id, env.id)
depl_1 = deployment.prepareAutoDeployeds(depl_1)
deployment.validate(depl_1)
taskid = deployment.createDeployTask(depl_1).id
deployit.startTaskAndWait(taskid)

# assert mappings

depl = deployment.prepareInitial(shopFrontendPackage_1_0.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
depl.deployedApplication.values['orchestrator'] = ['sequential-by-dependency']

assertEquals(1, len(depl.deployeds))
assertEquals(1, len(depl.requiredDeployments))
assertEquals(2, len(depl.requiredDeployments[0].deployeds))
assertEquals("frontendDeployable", depl.deployeds[0].name)
requiredDeployedNames = map(lambda deployed: deployed.name, depl.requiredDeployments[0].deployeds)
assertTrue("backendDeployableAdditional" in requiredDeployedNames)
assertTrue("backendDeployable" in requiredDeployedNames)

# task preview

previewBlock = deployment.taskPreviewBlock(depl)

assertEquals(2, len(previewBlock.blocks[0].block.blocks))

assertTrue("app-dependencies-ShopBackend" in previewBlock.blocks[0].block.blocks[0].description)
assertTrue("app-dependencies-ShopFrontend" in previewBlock.blocks[0].block.blocks[1].description)

# cache hit to remove workdir
deployment.validate(depl)

# execute the deployment
taskid = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskid)

# check if deployment created all CIs
assertTrue(repository.exists(depl.deployedApplication.id))
assertTrue(repository.exists(depl.deployeds[0].id))
assertTrue(repository.exists(depl.requiredDeployments[0].deployedApplication.id))
assertTrue(repository.exists(depl.requiredDeployments[0].deployeds[0].id))
assertTrue(repository.exists(depl.requiredDeployments[0].deployeds[1].id))

# should be able to individually undeploy the application in the right order

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

undeployTask = deployment.createUndeployTask(depl.requiredDeployments[0].deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

# check undeployment is succesfull
assertEquals(False, repository.exists(depl_1.deployedApplication.id))
assertEquals(False, repository.exists(depl.deployedApplication.id))
assertEquals(False, repository.exists(depl.requiredDeployments[0].deployedApplication.id))
