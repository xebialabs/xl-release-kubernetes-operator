env1 = repository.create(factory.configurationItem('Environments/repo-env1', 'udm.Environment', {"tags":["t1"]}))
dict1 = factory.configurationItem('Environments/repo-dict1', 'udm.Dictionary', {})

assertNotNone(env1._ci_attributes)

created_at = env1._ci_attributes.createdAt

assertEquals("admin", env1._ci_attributes.createdBy)
assertNotNone(created_at)
assertEquals("admin", env1._ci_attributes.lastModifiedBy)
assertNotNone(env1._ci_attributes.lastModifiedAt)

env1.dictionaries = ["Environments/repo-dict1"]

repository.update([env1, dict1])
env1 = repository.read('Environments/repo-env1')

assertEquals("admin", env1._ci_attributes.createdBy)
assertEquals(created_at, env1._ci_attributes.createdAt)
assertEquals("admin", env1._ci_attributes.lastModifiedBy)
assertTrue(created_at != env1._ci_attributes.lastModifiedAt)

repository.delete(env1.id)
repository.delete(dict1.id)
