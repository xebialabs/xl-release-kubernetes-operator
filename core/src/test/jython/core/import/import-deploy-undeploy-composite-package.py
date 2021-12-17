yak_server = create_random_yak_server('yakserver-undeploy-composite')
env = create_random_environment('yakEnv-undeploy-composite', [yak_server.id])

importPackage('GrazingApp/3.0')
grazing_app = repository.read('Applications/GrazingApp/3.0')
assertNotNone(grazing_app)

importPackage('RepoApp/1.0')
file_app = repository.read('Applications/RepoApp/1.0')
assertNotNone(file_app)

#now import the composite package
importPackage('CompositeApp/1.0')
composite_app = repository.read('Applications/CompositeApp/1.0')
assertNotNone(composite_app)

depl = deployment.prepareInitial(composite_app.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

assertNotNone(repository.read("%s/CompositeApp" % env.id))
assertNotNone(repository.read('%s/test.yak' % yak_server.id))
assertNotNone(repository.read('%s/test.yak1' % yak_server.id))

undeployTask = deployment.createUndeployTask(depl.deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)
