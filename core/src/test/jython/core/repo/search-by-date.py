from java.util import Calendar

env1 = repository.create(factory.configurationItem('Environments/repo-by-date-an-env1','udm.Environment'))
env2 = repository.create(factory.configurationItem('Environments/repo-by-date-an-env2','udm.Environment'))

now = Calendar.getInstance()
envsResult = repository.search('udm.Environment', now)

assertTrue(env1.id in envsResult)
assertTrue(env2.id in envsResult)
assertTrue(len(envsResult) >= 2)

now.add(Calendar.MINUTE, -1)
envsResult2 = repository.search('udm.Environment', now)
assertFalse(env1.id in envsResult2)
assertFalse(env2.id in envsResult2)

repository.delete(env1.id)
repository.delete(env2.id)
