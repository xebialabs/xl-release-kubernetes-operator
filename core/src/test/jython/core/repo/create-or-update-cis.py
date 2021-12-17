env1 = repository.create(factory.configurationItem('Environments/repo-env1', 'udm.Environment', {"tags":["t1"]}))
env2 = factory.configurationItem('Environments/repo-env2', 'udm.Environment', {"tags":["t2"]})
dict1 = factory.configurationItem('Environments/repo-dict1', 'udm.Dictionary', {})


env1.dictionaries = ["Environments/repo-dict1"]

repository.update([env1,env2, dict1])

assertTrue(repository.exists(env2.id))
assertTrue(repository.exists(dict1.id))
assertEquals("Environments/repo-dict1", repository.read(env1.id).dictionaries[0])

repository.delete(env1.id)
repository.delete(env2.id)
repository.delete(dict1.id)

