from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

app = create_random_application('rollback-PortalApp')
repository.create(factory.configurationItem('%s/1.0' % app, 'udm.DeploymentPackage'))
repository.create(factory.configurationItem('%s/1.0/PortalWar' % app, 'test-v3.PortalWar'))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet1' % app, 'test-v3.Portlet', {'portletName':'{{PortletOneName}}'}))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet2' % app, 'test-v3.Portlet', {'portletName':'PortletTwo'}))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet2/Settings1' % app,'test-v3.PortletSettings', {'mySetting':'myValue'}))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet2/Settings2' % app, 'test-v3.PortletSettings', {'mySetting':'myValue'}))

server = create_random_dummy_server()
dict = create_random_dict({'entries': {'PortletOneName':'PortletOne'}})
env = create_random_environment('rollback-dummyEnv', [server.id], [dict.id])

repository.create(factory.configurationItem('%s/2.0' % app, 'udm.DeploymentPackage'))
repository.create(factory.configurationItem('%s/2.0/PortalWar' % app, 'test-v3.PortalWar'))
repository.create(factory.configurationItem('%s/2.0/PortalWar/Portlet3' % app, 'test-v3.Portlet', {'portletName':'PortletThree'}))
repository.create(factory.configurationItem('%s/2.0/PortalWar/Portlet2' % app, 'test-v3.Portlet', {'portletName':'PortletTwo'}))
repository.create(factory.configurationItem('%s/2.0/PortalWar/Portlet2/Settings3' % app, 'test-v3.PortletSettings', {'mySetting':'myValue'}))
repository.create(factory.configurationItem('%s/2.0/PortalWar/Portlet2/Settings2' % app, 'test-v3.PortletSettings', {'mySetting':'myValue'}))

depl = deployment.prepareInitial('%s/1.0' % app, env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals(5, len(depl.deployeds))

map = {}
for d in depl.deployeds:
    map[d.id] = d

assertTrue('%s/PortalWar' % server.id in map)
assertTrue('%s/PortalWar/Portlet1' % server.id in map)
assertTrue('%s/PortalWar/Portlet2' % server.id in map)
assertTrue('%s/PortalWar/Portlet2/Settings1' % server.id in map)
assertTrue('%s/PortalWar/Portlet2/Settings2' % server.id in map)

taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

udepl = deployment.prepareUpgrade('%s/2.0' % app.id, depl.deployedApplication.id)
assertEquals(5, len(depl.deployeds))

umap = {}
for d in udepl.deployeds:
    umap[d.id] = d

assertTrue('%s/PortalWar' % server.id in umap)
assertTrue('%s/PortalWar/Portlet3' % server.id in umap)
assertTrue('%s/PortalWar/Portlet2' % server.id in umap)
assertTrue('%s/PortalWar/Portlet2/Settings3' % server.id in umap)
assertTrue('%s/PortalWar/Portlet2/Settings2' % server.id in umap)

utaskid = deployment.createDeployTask(udepl).id
task2.start(utaskid)
wait_for_task_state(utaskid, TaskExecutionState.EXECUTED)

rtaskid = deployment.createRollbackTask(utaskid).id

deployit.startTaskAndWait(rtaskid)
wait_for_task_state(rtaskid, TaskExecutionState.DONE)
