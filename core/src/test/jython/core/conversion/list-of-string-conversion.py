app = create_random_application('conversion-orchestrator-App')
ci = repository.create(factory.configurationItem('%s/1.0' % app.id, 'udm.DeploymentPackage', {}))

ci.orchestrator = ['default', 'container-by-container']
ci = repository.update(ci)
assertEquals(2, ci.orchestrator.size())
assertEquals('default', ci.orchestrator.get(0))
assertEquals('container-by-container', ci.orchestrator.get(1))

ci.orchestrator = 'default'
ci = repository.update(ci)
assertEquals(1, ci.orchestrator.size())
assertEquals('default', ci.orchestrator.get(0))
