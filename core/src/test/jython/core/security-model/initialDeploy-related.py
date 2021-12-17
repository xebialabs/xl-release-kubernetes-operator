aenv = repository.create(factory.configurationItem('Environments/security-model-dir/security-model-env1', 'udm.Environment', {}))

def tryRead():
	switchUser('security-model-user')

	try:
		repository.read(aenv.id)
	except:
		switchUser('admin')
	else:
		raise Exception('Should not be allowed to read env')

def doRead():
	switchUser('security-model-user')
	repository.read(aenv.id)
	switchUser('admin')


tryRead()
security.grant('deploy#initial', 'security-model-user', ['Environments/security-model-dir'])
doRead()
security.revoke('deploy#initial', 'security-model-user', ['Environments/security-model-dir'])
tryRead()
security.grant('deploy#upgrade', 'security-model-user', ['Environments/security-model-dir'])
doRead()
security.revoke('deploy#upgrade', 'security-model-user', ['Environments/security-model-dir'])
tryRead()

repository.delete(aenv.id)