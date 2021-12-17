
created = repository.create(factory.configurationItem('Infrastructure/security-model-dir/security-model-host1', 'test-v3.DummyJeeServer', {'hostName':'localhost'}))
security.grant('repo#edit','security-model-user', ['Infrastructure/security-model-dir'])

switchUser('security-model-user')

try:
	repository.read(created.id)
except:
	switchUser('admin')
else:
	raise Exception("should not be able to access")

security.grant('read','security-model-user', ['Infrastructure/security-model-dir'])

switchUser('security-model-user')

host = repository.read(created.id)
host.hostName = 'Knutselsmurf'
repository.update(host)
host = repository.read(host.id)

switchUser('admin')

security.revoke('repo#edit', 'security-model-user', ['Infrastructure/security-model-dir'])

switchUser('security-model-user')

host.hostName = 'Lolsmurf'

try:
	repository.update(host)
except:
	switchUser('admin')
else:
	raise Exception("should not be able to access")

security.grant('repo#edit', 'security-model-user', ['Infrastructure/security-model-dir'])

switchUser('security-model-user')

repository.update(host)

switchUser('admin')

security.revoke('repo#edit', 'security-model-user', ['Infrastructure/security-model-dir'])
security.revoke('read', 'security-model-user', ['Infrastructure/security-model-dir'])
