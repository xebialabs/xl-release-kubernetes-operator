newHost = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host", "test-v3.DummyJeeServer", {'hostName':'localhost'}))
switchUser('security-model-user')

try:
	repository.read(newHost.id)
except:
	switchUser('admin')
else:
	raise Exception("Not allowed to read")

security.grant('read', 'security-model-user', ['Infrastructure/security-model-dir'])

switchUser('security-model-user')

repository.read(newHost.id)

switchUser('admin')

security.revoke('read', 'security-model-user', ['Infrastructure/security-model-dir'])
security.grant('admin', 'security-model-user')

switchUser('security-model-user')

repository.read(newHost.id)

switchUser('admin')
security.revoke('admin', 'security-model-user')
