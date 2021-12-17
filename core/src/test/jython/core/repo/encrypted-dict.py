dict = repository.create(factory.configurationItem('Environments/repo-encryptedDict', 'udm.EncryptedDictionary',{'entries':{'password':'secret'}}))

if (dict.entries['password'] == 'secret'):
	raise Exception('Should have obfuscated encrypted dictionary value %s' % dict.entries)

repository.delete(dict.id)
