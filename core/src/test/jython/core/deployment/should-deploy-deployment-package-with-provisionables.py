provisioned_container_app_pkg = repository.read('Applications/DeploymentAppWithProvisionables/1.0')
yak_server = create_random_yak_server('best-yakserver')
env = create_random_environment('yakEnv-package-with-provisionables', [yak_server.id])

depl = deployment.prepareInitial(provisioned_container_app_pkg.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

provisioned1 = repository.read("%s/yakBucket" % yak_server.id)
assertNotNone(provisioned1)

deployedTestYak = repository.read('%s/file1' % yak_server.id)
assertNotNone(deployedTestYak)
