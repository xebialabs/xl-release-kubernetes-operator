app = repository.create(factory.configurationItem('Applications/issues-PortalApp-4514','udm.Application'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4514/1.0','udm.DeploymentPackage'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4514/1.0/PortalWar','test-v3.PortalWar'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4514/1.0/PortalWar/Portlet1','test-v3.Portlet'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4514/1.0/PortalWar/Portlet2','test-v3.Portlet'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4514/1.0/PortalWar/Portlet2/Settings1','test-v3.PortletSettings'))
repository.create(factory.configurationItem('Applications/issues-PortalApp-4514/1.0/PortalWar/Portlet2/Settings2','test-v3.PortletSettings'))

server = repository.create(factory.configurationItem('Infrastructure/issues-dummyServer-4514','test-v3.DummyJeeServer',{'hostName':'Dummy'}))
env = repository.create(factory.configurationItem('Environments/issues-dummyEnv-4514','udm.Environment',{'members':[server.id]}))

depl = deployment.prepareInitial('Applications/issues-PortalApp-4514/1.0',env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals(5, len(depl.deployeds))

depl = deployment.validate(depl)

assertEquals(0, len(depl.deployeds[0].validations))
assertEquals(1, len(depl.deployeds[1].validations))
assertEquals(1, len(depl.deployeds[2].validations))
assertEquals(1, len(depl.deployeds[3].validations))
assertEquals(1, len(depl.deployeds[4].validations))

repository.delete(env.id)
repository.delete(server.id)
repository.delete(app.id)
