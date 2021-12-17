app = repository.create(factory.configurationItem('Applications/issues-PortalApp-4739','udm.Application'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4739/1.0','udm.DeploymentPackage'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4739/1.0/PortalWar','test-v3.PortalWar'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4739/1.0/PortalWar/Portlet1','test-v3.Portlet'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4739/1.0/PortalWar/Portlet2','test-v3.Portlet'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4739/1.0/PortalWar/Portlet2/Settings1','test-v3.PortletSettings'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4739/1.0/PortalWar/Portlet2/Settings2','test-v3.PortletSettings'))

server = repository.create(factory.configurationItem('Infrastructure/issues-dummyServer-4739','test-v3.DummyJeeServer',{'hostName':'Dummy'}))
env = repository.create(factory.configurationItem('Environments/issues-dummyEnv-3','udm.Environment',{'members':[server.id]}))

depl = deployment.prepareInitial('Applications/issues-PortalApp-4739/1.0',env.id)
depl = deployment.prepareAutoDeployeds(depl)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals(5, len(depl.deployeds))

depl = deployment.validate(depl)

repository.delete(env.id)
repository.delete(server.id)
repository.delete(app.id)
