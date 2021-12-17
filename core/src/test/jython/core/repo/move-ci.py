env = repository.create(factory.configurationItem('Environments/repo-env-move', 'udm.Environment', {}))
group = repository.create(factory.configurationItem('Environments/repo-prodGroup', 'core.Directory', {}))

repository.move(env, group.id + '/repo-move')
assertNotNone(repository.read(group.id + '/repo-move'))

repository.rename(group.id + '/repo-move', 'repo-production')
assertNotNone(repository.read(group.id + '/repo-production'))

repository.delete(group.id)
