dictionary = repository.create(factory.configurationItem('Environments/repo-dict', 'udm.Dictionary'))
readDict = repository.read('Environments/repo-dict')

readDict.entries = {'foo':'bar'}

repository.update(readDict)

readDict.entries = {'foo':'baz'}

try:
    repository.update(readDict)
except:
    print('OK')
else:
    raise Exception("Should have raised conflict")

repository.delete(dictionary.id)
