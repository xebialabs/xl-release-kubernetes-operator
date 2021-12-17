from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

app = create_random_application('deployment-PortalApp')
repository.create(factory.configurationItem('%s/1.0' % app.id,'udm.DeploymentPackage'))
repository.create(factory.configurationItem('%s/1.0/PortalWar' % app.id,'test-v3.PortalWar'))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet1' % app.id,'test-v3.Portlet', {'portletName':'{{PortletOneName}}'}))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet2' % app.id,'test-v3.Portlet', {'portletName':'PortletTwo'}))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet2/Settings1' % app.id,'test-v3.PortletSettings', {'mySetting':'myValue'}))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet2/Settings2' % app.id,'test-v3.PortletSettings', {'mySetting':'myValue'}))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet2/Attributes1' % app.id,'test-v3.PortletAttributes', {'myAttribute':'myValue'}))
repository.create(factory.configurationItem('%s/1.0/PortalWar/Portlet2/Attributes2' % app.id,'test-v3.PortletAttributes', {'myAttribute':'myValue'}))
server = create_random_dummy_server()
dict1 = create_random_dict({'entries': {'PortletOneName':'PortletOne'}})
env1 = create_random_environment("env1", [server.id], [dict1.id])

depl = deployment.prepareInitial('%s/1.0' % app.id, env1.id)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals(7, len(depl.deployeds))

map = {}
for d in depl.deployeds:
    map[d.id] = d

assertTrue('%s/PortalWar' % server.id in map)
assertTrue('%s/PortalWar/Portlet1' % server.id in map)
assertTrue('%s/PortalWar/Portlet2' % server.id in map)
assertTrue('%s/PortalWar/Portlet2/Settings1' % server.id in map)
assertTrue('%s/PortalWar/Portlet2/Settings2' % server.id in map)
assertTrue('%s/PortalWar/Portlet2/Attributes1' % server.id in map)
assertTrue('%s/PortalWar/Portlet2/Attributes2' % server.id in map)

references = map['%s/PortalWar' % server.id].portlets
assertEquals(2, len(references))
for r in references:
    assertTrue(r in map)

settings = map['%s/PortalWar/Portlet2' % server.id].settings
assertEquals(2, len(settings))
for s in settings:
    assertTrue(s in map)

attributes = map['%s/PortalWar/Portlet2' % server.id].attributes
assertEquals(2, len(attributes))
for a in attributes:
    assertTrue(a in map)

task_id = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(task_id)
wait_for_task_state(task_id, TaskExecutionState.DONE)

assertTrue(repository.exists('%s/PortalWar' % server.id))
assertTrue(repository.exists('%s/PortalWar/Portlet1' % server.id))
assertTrue(repository.exists('%s/PortalWar/Portlet2' % server.id))
assertTrue(repository.exists('%s/PortalWar/Portlet2/Settings1' % server.id))
assertTrue(repository.exists('%s/PortalWar/Portlet2/Settings2' % server.id))
assertTrue(repository.exists('%s/PortalWar/Portlet2/Attributes1' % server.id))
assertTrue(repository.exists('%s/PortalWar/Portlet2/Attributes2' % server.id))
