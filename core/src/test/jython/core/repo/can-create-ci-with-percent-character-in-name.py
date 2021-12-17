app1 = repository.create(factory.configurationItem('Applications/AppForTest', 'udm.Application'))
assertTrue(repository.exists(app1.id))
try:
    repository.create(factory.configurationItem('Applications/AppForTest', 'udm.Application'))
except:
    pass
else:
    raise Exception('It should throw exception that application with the same name already exists')

app2 = repository.create(factory.configurationItem('Applications/App%ForTest', 'udm.Application'))
assertTrue(repository.exists(app2.id))
try:
    repository.create(factory.configurationItem('Applications/App%ForTest', 'udm.Application'))
except:
    pass
else:
    raise Exception('It should throw exception that application with the same name already exists')

app3 = repository.create(factory.configurationItem('Applications/App%%ForTest', 'udm.Application'))
assertTrue(repository.exists(app3.id))

app4 = repository.create(factory.configurationItem('Applications/app%fortest', 'udm.Application'))
assertTrue(repository.exists(app4.id))

repository.delete(app1.id)
repository.delete(app2.id)
repository.delete(app3.id)
repository.delete(app4.id)
