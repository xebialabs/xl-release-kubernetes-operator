security.createUser('security-model-developer2', DEFAULT_PASSWORD)
security.assignRole('security-model-developer2', ['security-model-developer2'])
security.grant('login', 'security-model-developer2')

repository.create(factory.configurationItem('Environments/security-model-dir2','core.Directory',{}))


host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'test-v3.DummyJeeServer', {'hostName':'localhost'}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))
host2 = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host2", 'test-v3.DummyJeeServer', {'hostName':'localhost'}))
env2 = repository.create(factory.configurationItem("Environments/security-model-dir2/security-model-env2", "udm.Environment", {'members':[host2.id]}))

switchUser('security-model-developer2')

try:
	repository.read('Environments/security-model-dir/security-model-env1')
except:
	switchUser('admin')
else:
	raise Exception("Should not have read permissions")


security.grant("read", "security-model-developer2", ['Environments/security-model-dir'])

switchUser('security-model-developer2')

repository.read('Environments/security-model-dir/security-model-env1')

try:
	repository.read('Environments/security-model-dir2/security-model-env2')
except:
	switchUser('admin')
else:
	raise Exception("Should not have read permissions")

switchUser('admin')

security.revoke("read", "security-model-developer2", ['Environments/security-model-dir'])
security.revoke("login", "security-model-developer2")

security.deleteUser('security-model-developer2')
security.removeRole('security-model-developer2')
repository.delete('Environments/security-model-dir2')