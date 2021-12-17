noContainer = repository.create(factory.configurationItem('Infrastructure/issues-noContainer','yak.NonContainerYakInfra',{}))

ci = repository.create(factory.configurationItem('Environments/issues-noEnv','udm.Environment',{'members':[noContainer.id]}))
assertFalse(repository.exists(ci.id))
assertEquals(1, len(ci.validations))

repository.delete(noContainer.id)