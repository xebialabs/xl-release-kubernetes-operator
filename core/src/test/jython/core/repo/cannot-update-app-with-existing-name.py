app = repository.create(factory.configurationItem('Applications/repo-existingForUpdate', 'udm.Application'))
try:
    repository.update(factory.configurationItem('Applications/repo-1/repo-existingForUpdate', 'udm.Application'))
except:
    pass
else:
    raise Exception('It should throw exception that application with the same name already exists')

repository.delete(app.id)
