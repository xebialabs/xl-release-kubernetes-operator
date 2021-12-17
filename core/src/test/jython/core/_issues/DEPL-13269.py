# Shows both the bug in DEPL-13269 and the inconsistency in DEPL-13431

app = repository.create(factory.configurationItem('Applications/issues-PortalApp-13269','udm.Application'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-13269/1.0','udm.DeploymentPackage'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-13269/1.0/PortalWar','test-v3.PortalWar'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-13269/1.0/PortalWar/Portlet1','test-v3.Portlet',{'portletName':'p1'}))

server = repository.create(factory.configurationItem('Infrastructure/issues-dummyServer-13269','test-v3.DummyJeeServer',{'hostName':'Dummy'}))
env = repository.create(factory.configurationItem('Environments/issues-dummyEnv-13269','udm.Environment',{'members':[server.id]}))

depl = deployment.prepareInitial('Applications/issues-PortalApp-13269/1.0',env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

task2.addPause(taskId, "0_1_1_2")
deployit.startTaskAndWait(taskId)

wait_for_task_state(taskId, TaskExecutionState.STOPPED)

# DEPL-13269: Cancellation fails because of referred embedded child not being stored
task2.cancel(taskId)


# DEPL-13431: Read fails because portlet (embedded) not being stored
portlet = repository.read('Infrastructure/issues-dummyServer-13269/PortalWar/Portlet1')
assertNotNone(portlet)

repository.delete(env.id)
repository.delete(server.id)
repository.delete(app.id)
