app = repository.create(factory.configurationItem('Applications/repo-test-name', 'udm.Application'))
assertTrue(repository.exists(app.id))
env = repository.create(factory.configurationItem('Environments/repo-test-name', 'udm.Environment'))
assertTrue(repository.exists(env.id))

repository.delete(app.id)
repository.delete(env.id)
