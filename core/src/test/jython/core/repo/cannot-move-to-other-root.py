group = repository.create(factory.configurationItem('Environments/repo-prodGroup', 'core.Directory', {}))
group2 = repository.create(factory.configurationItem('Environments/repo-devGroup', 'core.Directory', {}))
group3 = repository.create(factory.configurationItem('Environments/repo-devGroup/team1', 'core.Directory', {}))
group4 = repository.create(factory.configurationItem('Infrastructure/repo-devGroup', 'core.Directory', {}))

repository.move(group3.id, group.id + "/" + group3.name)

try:
  repository.move(group.id + "/" + group3.name, group4.id + "/" + group3.name)
except:
  pass
else:
  raise Exception("Cannot move there.")


repository.delete(group.id)
repository.delete(group2.id)
repository.delete(group4.id)
