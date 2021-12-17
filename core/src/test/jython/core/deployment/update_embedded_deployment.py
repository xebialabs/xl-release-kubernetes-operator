from com.xebialabs.deployit.core.util import CiUtils
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

app = create_random_application("deployment-PortalApp")
app1_0 = repository.create(factory.configurationItem('%s/1.0' % app.id, 'udm.DeploymentPackage'))
repository.create(factory.configurationItem('%s/PortalWar' % app1_0.id, 'test-v3.PortalWar'))
repository.create(factory.configurationItem('%s/PortalWar/Portlet1' % app1_0.id, 'test-v3.Portlet', {'portletName':'{{PortletOneName}}'}))
repository.create(factory.configurationItem('%s/PortalWar/Portlet2' % app1_0.id, 'test-v3.Portlet', {'portletName':'PortletTwo'}))
repository.create(factory.configurationItem('%s/PortalWar/Portlet2/Settings1' % app1_0.id, 'test-v3.PortletSettings', {'mySetting':'myValue'}))
repository.create(factory.configurationItem('%s/PortalWar/Portlet2/Settings2' % app1_0.id, 'test-v3.PortletSettings', {'mySetting':'myValue'}))

server = create_random_dummy_server()
dict1 = create_random_dict({'entries': {'PortletOneName':'PortletOne'}})
env = create_random_environment('env1', [server.id], [dict1.id])

app2_0 = repository.create(factory.configurationItem('%s/2.0' % app.id, 'udm.DeploymentPackage'))
repository.create(factory.configurationItem('%s/PortalWar' % app2_0.id, 'test-v3.PortalWar'))
repository.create(factory.configurationItem('%s/PortalWar/Portlet3' % app2_0.id, 'test-v3.Portlet', {'portletName':'PortletThree'}))
repository.create(factory.configurationItem('%s/PortalWar/Portlet2' % app2_0.id, 'test-v3.Portlet', {'portletName':'PortletTwo'}))
repository.create(factory.configurationItem('%s/PortalWar/Portlet2/Settings3' % app2_0.id, 'test-v3.PortletSettings', {'mySetting':'myValue'}))
repository.create(factory.configurationItem('%s/PortalWar/Portlet2/Settings2' % app2_0.id, 'test-v3.PortletSettings', {'mySetting':'myValue'}))

depl = deployment.prepareInitial(app1_0.id, env.id)
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

udepl = deployment.prepareUpgrade(app2_0.id, "%s/%s" % (env.id, CiUtils.getName(app.id)))
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
deployit.startTaskAndWait(utaskid)
wait_for_task_state(utaskid, TaskExecutionState.DONE)
