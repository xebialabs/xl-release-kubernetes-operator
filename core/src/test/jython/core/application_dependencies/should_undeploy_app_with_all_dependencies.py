# prepare data
shopFrontendApp1 = create_random_application("app-dependencies-ShopFrontend")
shopBackendApp1 = create_random_application("app-dependencies-ShopBackend")
shopServicesApp1 = create_random_application('app-dependencies-ShopServices')
shopDatabaseApp1 = create_random_application('app-dependencies-ShopDatabase')
env = create_random_environment_with_yak_server("env1")

shopFrontendPackage = repository.create(
    factory.configurationItem('%s/1.0' % shopFrontendApp1.id, 'udm.DeploymentPackage',
                              {"applicationDependencies": {shopBackendApp1.name: "1.0", shopServicesApp1.name: "1.0"}}))
frontendDeployable = repository.create(
    factory.configurationItem('%s/frontendDeployable' % shopFrontendPackage.id, 'yak.YakConfigurationSpec', {}))


shopBackendPackage = repository.create(
    factory.configurationItem('%s/1.0' % shopBackendApp1.id, 'udm.DeploymentPackage',
                              {"applicationDependencies": {shopServicesApp1.name: "1.0"}}))

backendDeployable = repository.create(
    factory.configurationItem('%s/backendDeployable' % shopBackendPackage.id, 'yak.YakConfigurationSpec', {}))


shopServicesPackage = repository.create(
    factory.configurationItem('%s/1.0' % shopServicesApp1.id, 'udm.DeploymentPackage',
                              {"applicationDependencies": {shopDatabaseApp1.name: "1.0"}}))

servicesDeployable = repository.create(
    factory.configurationItem('%s/servicesDeployable' % shopServicesPackage.id, 'yak.YakConfigurationSpec', {}))


shopDatabasePackage = repository.create(
    factory.configurationItem('%s/1.0' % shopDatabaseApp1.id, 'udm.DeploymentPackage', {}))

databaseDeployable = repository.create(
    factory.configurationItem('%s/databaseDeployable' % shopDatabasePackage.id, 'yak.YakConfigurationSpec', {}))

depl = deployment.prepareInitial(shopFrontendPackage.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
depl.deployedApplication.values['orchestrator'] = ['sequential-by-dependency']
deploy_task_id = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(deploy_task_id)

assertTrue(repository.exists(depl.deployedApplication.id))
assertTrue(repository.exists(depl.requiredDeployments[0].deployedApplication.id))
assertTrue(repository.exists(depl.requiredDeployments[1].deployedApplication.id))
assertTrue(repository.exists(depl.requiredDeployments[2].deployedApplication.id))

un_deployment = proxies.getDeployment().prepareUndeploy(depl.deployedApplication.id)
un_deployment.deployedApplication.setProperty("undeployDependencies", True)
undeploy_task_id = proxies.getDeployment().createTask(un_deployment)

deployit.startTaskAndWait(undeploy_task_id)

assertFalse(repository.exists(depl.deployedApplication.id))
assertFalse(repository.exists(depl.requiredDeployments[0].deployedApplication.id))
assertFalse(repository.exists(depl.requiredDeployments[1].deployedApplication.id))
assertFalse(repository.exists(depl.requiredDeployments[2].deployedApplication.id))
