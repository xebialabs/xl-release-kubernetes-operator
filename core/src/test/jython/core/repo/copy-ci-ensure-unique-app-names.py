#
repository.create(factory.configurationItem('Applications/repo-apps', 'core.Directory'))
repository.create(factory.configurationItem('Applications/repo-apps/repo-pet-1', 'core.Directory'))
repository.create(factory.configurationItem('Applications/repo-apps/repo-pet-1/repo-pet-app-1', 'udm.Application'))
repository.create(factory.configurationItem('Applications/repo-apps/repo-pet-2', 'core.Directory'))
repository.create(factory.configurationItem('Applications/repo-apps/repo-pet-2/repo-pet-app-2', 'udm.Application'))

repository.create(factory.configurationItem('Applications/repo-pet-app-1 Copy', 'udm.Application'))

try:
    repository.copy('Applications/repo-apps', 'Applications/repo-apps 2')
    assertTrue(repository.exists('Applications/repo-apps 2'), 'Applications/repo-apps 2')
    assertFalse(repository.exists('Applications/repo-apps 2/repo-pet-1/repo-pet-app-1'), 'Applications/repo-apps 2/repo-pet-1/repo-pet-app-1')
    assertTrue(repository.exists('Applications/repo-apps 2/repo-pet-1/repo-pet-app-1 Copy Copy'), 'Applications/repo-apps 2/repo-pet-1/repo-pet-app-1 Copy Copy')
    assertFalse(repository.exists('Applications/repo-apps 2/repo-pet-2/repo-pet-app-2'), 'Applications/repo-apps 2/repo-pet-2/repo-pet-app-2')
    assertTrue(repository.exists('Applications/repo-apps 2/repo-pet-2/repo-pet-app-2 Copy'), 'Applications/repo-apps 2/repo-pet-2/repo-pet-app-2 Copy')
finally:
    repository.delete('Applications/repo-apps')
    repository.delete('Applications/repo-apps 2')
    repository.delete('Applications/repo-pet-app-1 Copy')
