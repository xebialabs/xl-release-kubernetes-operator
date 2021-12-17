yak = repository.create(factory.configurationItem('Infrastructure/issues-yak','yak.YakServerWithDefault',{}))
assertEquals("localhost", yak.values['hostname'])

yak.values['hostname'] = ''
yak2 = repository.update(yak)

assertEquals("", yak2.values['hostname'])

repository.delete(yak2.id)