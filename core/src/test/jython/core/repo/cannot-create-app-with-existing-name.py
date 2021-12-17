app = repository.create(factory.configurationItem('Applications/repo-existingForCreation', 'udm.Application'))
try:
    repository.create(factory.configurationItem('Applications/repo-1/repo-existingForCreation', 'udm.Application'))
except:
    pass
else:
    raise Exception('It should throw exception that application with the same name already exists')

repository.delete(app.id)
