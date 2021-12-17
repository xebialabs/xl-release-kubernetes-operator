# prepare data
shopFrontendApp1 = create_random_application("app-dependencies-ShopFrontend")
shopBackendApp1 = create_random_application("app-dependencies-ShopBackend")
shopServicesApp1 = create_random_application("app-dependencies-ShopServices")
shopDatabaseApp1 = create_random_application("app-dependencies-ShopDatabase")
env = create_random_environment_with_yak_server("env1")

shopFrontendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopFrontendApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopBackendApp1.name: "1.0", shopServicesApp1.name: "1.5"}}))
shopBackendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopBackendApp1.id, 'udm.DeploymentPackage',  {"applicationDependencies": {shopServicesApp1.name: "[1.0, 2.0)"}}))
shopServicesPackage_1_5 = repository.create(factory.configurationItem('%s/1.5' % shopServicesApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopDatabaseApp1.name: "[1.0, 3.0]"}}))
shopDatabasePackage_2_0 = repository.create(factory.configurationItem('%s/2.0' % shopDatabaseApp1.id, 'udm.DeploymentPackage', {}))

backendDeployable = repository.create(factory.configurationItem('%s/backendDeployable' % shopBackendPackage_1_0.id, 'yak.YakConfigurationSpec', {}))
frontendDeployable = repository.create(factory.configurationItem('%s/frontendDeployable' % shopFrontendPackage_1_0.id, 'yak.YakConfigurationSpec', {}))
servicesDeployable = repository.create(factory.configurationItem('%s/servicesDeployable' % shopServicesPackage_1_5.id, 'yak.YakConfigurationSpec', {}))
databaseDeployable = repository.create(factory.configurationItem('%s/databaseDeployable' % shopDatabasePackage_2_0.id, 'yak.YakConfigurationSpec', {}))

# prepare deployment
depl = deployment.prepareInitial(shopFrontendPackage_1_0.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
depl.deployedApplication.values['orchestrator'] = ['sequential-by-dependency']

# assert mappings
assertEquals(1, len(depl.deployeds))
assertEquals(3, len(depl.requiredDeployments))
assertEquals(1, len(depl.requiredDeployments[0].deployeds))
assertEquals(1, len(depl.requiredDeployments[1].deployeds))
assertEquals(1, len(depl.requiredDeployments[2].deployeds))
assertEquals("databaseDeployable", depl.requiredDeployments[0].deployeds[0].name)
assertEquals("servicesDeployable", depl.requiredDeployments[1].deployeds[0].name)
assertEquals("backendDeployable", depl.requiredDeployments[2].deployeds[0].name)
assertEquals("frontendDeployable", depl.deployeds[0].name)


# task preview

previewBlock = deployment.taskPreviewBlock(depl)

assertEquals(4, len(previewBlock.blocks[0].block.blocks))

assertTrue("app-dependencies-ShopDatabase" in previewBlock.blocks[0].block.blocks[0].description)
assertTrue("app-dependencies-ShopServices" in previewBlock.blocks[0].block.blocks[1].description)
assertTrue("app-dependencies-ShopBackend" in previewBlock.blocks[0].block.blocks[2].description)
assertTrue("app-dependencies-ShopFrontend" in previewBlock.blocks[0].block.blocks[3].description)

# cache hit to remove workdir
deployment.validate(depl)

# execute the deployment
taskid = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskid)

# check if deployment created all CIs
assertTrue(repository.exists(depl.deployedApplication.id))
assertTrue(repository.exists(depl.deployeds[0].id))
assertTrue(repository.exists(depl.requiredDeployments[0].deployedApplication.id))
assertTrue(repository.exists(depl.requiredDeployments[1].deployeds[0].id))
assertTrue(repository.exists(depl.requiredDeployments[1].deployedApplication.id))
assertTrue(repository.exists(depl.requiredDeployments[1].deployeds[0].id))
assertTrue(repository.exists(depl.requiredDeployments[2].deployedApplication.id))
assertTrue(repository.exists(depl.requiredDeployments[2].deployeds[0].id))

# should be able to individually undeploy the application in the right order

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

undeployTask = deployment.createUndeployTask(depl.requiredDeployments[2].deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

undeployTask = deployment.createUndeployTask(depl.requiredDeployments[1].deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

undeployTask = deployment.createUndeployTask(depl.requiredDeployments[0].deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

# check un-deployment is successful
assertEquals(False, repository.exists(depl.deployedApplication.id))
assertEquals(False, repository.exists(depl.requiredDeployments[2].deployedApplication.id))
assertEquals(False, repository.exists(depl.requiredDeployments[1].deployedApplication.id))
assertEquals(False, repository.exists(depl.requiredDeployments[0].deployedApplication.id))
