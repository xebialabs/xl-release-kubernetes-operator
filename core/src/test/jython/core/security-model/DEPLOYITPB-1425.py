created = repository.create(factory.configurationItem('Infrastructure/security-model-dir/host1', 'test-v3.DummyJeeServer', {'hostName':'localhost'}))

security.createUser('security-model-foo-user', DEFAULT_PASSWORD)
security.assignRole('security-model-foo-user', ['security-model-foo-user'])
security.grant('login','security-model-foo-user')
security.grant('read','security-model-foo-user', ['Infrastructure/security-model-dir'])

switchUser('security-model-foo-user')

host = repository.read(created.id)
host.hostName = 'Knutselsmurf'

try:
	repository.update(host)
except:
	switchUser('admin')
else:
	raise Exception("Should not be allowed to update")

security.grant('repo#edit', 'security-model-foo-user', ['Infrastructure/security-model-dir'])

switchUser('security-model-foo-user')

repository.update(host)

switchUser('admin')
security.revoke('read', 'security-model-foo-user', ['Infrastructure/security-model-dir'])
security.revoke('repo#edit', 'security-model-foo-user', ['Infrastructure/security-model-dir'])
security.revoke('login','security-model-foo-user')

security.deleteUser('security-model-foo-user')
security.removeRole('security-model-foo-user')
