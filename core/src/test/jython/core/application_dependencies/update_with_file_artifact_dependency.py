from com.xebialabs.deployit.core.util import CiUtils

host = create_random_host("testhost")
env = create_random_environment("explicitEnv", [host.id])

# prepare data
shopFrontendApp1 = create_random_application("app-dependencies-ShopFrontend")
shopBackendApp1 = create_random_application("app-dependencies-ShopBackend")
shopServicesApp1 = create_random_application('app-dependencies-ShopServices')
shopDatabaseApp1 = create_random_application('app-dependencies-ShopDatabase')

shopBackendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopBackendApp1.id, 'udm.DeploymentPackage', {}))
shopBackendPackage_2_0 = repository.create(factory.configurationItem('%s/2.0' % shopBackendApp1.id, 'udm.DeploymentPackage', {}))
shopFrontendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopFrontendApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopBackendApp1.name: "1.0"}}))
shopFrontendPackage_2_0 = repository.create(factory.configurationItem('%s/2.0' % shopFrontendApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopBackendApp1.name: "2.0"}}))

file1 = createFile(shopBackendPackage_1_0.id, "file-1", "my-file-1.txt", "Test content1")
file2 = createFile(shopFrontendPackage_1_0.id, "file-2", "my-file-2.txt", "Test content2")
file3 = createFile(shopBackendPackage_2_0.id, "file-3", "my-file-3.txt", "Test content3")
file4 = createFile(shopFrontendPackage_2_0.id, "file-4", "my-file-4.txt", "Test content4")

# deploy shopFrontendPackage_1_0
initialDeployment = deployment.prepareInitial(shopFrontendPackage_1_0.id, env.id)
initialDeployment = deployment.prepareAutoDeployeds(initialDeployment)

initialDeployment.deployedApplication.values['orchestrator'] = ['sequential-by-dependency']
deployment.validate(initialDeployment)

assertEquals(1, len(initialDeployment.deployeds))
assertEquals(1, len(initialDeployment.requiredDeployments))
assertEquals(1, len(initialDeployment.requiredDeployments[0].deployeds))

taskid = deployment.createDeployTask(initialDeployment).id
deployit.startTaskAndWait(taskid)

#Doing un update
deploymentUpdate = deployment.prepareUpgrade(shopFrontendPackage_2_0.id, initialDeployment.deployedApplication.id)
deploymentUpdate = deployment.prepareAutoDeployeds(deploymentUpdate)
deploymentUpdate.deployedApplication.values['orchestrator'] = ['sequential-by-dependency']


# task preview
previewBlock = deployment.taskPreviewBlock(deploymentUpdate)

assertEquals(2, len(previewBlock.blocks[0].block.blocks))
assertEquals(2, len(previewBlock.blocks))

assertEquals(2, len(previewBlock.blocks[0].block.blocks[0].steps))

assertTrue(next((block for block in previewBlock.blocks[0].block.blocks if "%s 2.0" % CiUtils.getName(shopBackendApp1.id) in block.description)) is not None)
assertTrue(next((block for block in previewBlock.blocks[0].block.blocks if "%s 2.0" % CiUtils.getName(shopFrontendApp1.id) in block.description)) is not None)

blockId = previewBlock.blocks[0].block.blocks[0].id

previewStep1 = deployment.taskPreviewBlock(deploymentUpdate, blockId, 1)
assertTrue("Delete file-1" in previewStep1.description)

previewStep2 = deployment.taskPreviewBlock(deploymentUpdate, blockId, 2)
assertTrue("Copy file-3" in previewStep2.description)

deployment.validate(deploymentUpdate)

undeployTask = deployment.createUndeployTask(initialDeployment.deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)
