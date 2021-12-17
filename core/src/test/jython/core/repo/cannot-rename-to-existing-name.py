app = repository.create(factory.configurationItem('Applications/repo-existingForRenaming', 'udm.Application'))
try:
    repository.rename('Applications/repo-foo','repo-existingForRenaming')
except:
    pass
else:
    raise Exception('It should throw exception that application with the same name already exists')

repository.delete(app.id)
