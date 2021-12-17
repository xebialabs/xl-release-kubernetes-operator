env = repository.create(factory.configurationItem('Environments/repo-env-copy', 'udm.Environment', {}))

env2 = repository.copy(env.id, 'Environments/repo-env-copy2')
assertNotNone(env2)
assertNotNone(repository.read('Environments/repo-env-copy'))
assertNotNone(repository.read('Environments/repo-env-copy2'))

repository.delete(env.id)
repository.delete(env2.id)
