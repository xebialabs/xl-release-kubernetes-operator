host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'test-v3.DummyJeeServer', {'hostName':'localhost'}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))

switchUser('security-model-user')

try:
	repository.read(host.id)
except:
	switchUser('admin')
else:
	raise Exception("Not allowed to read")

security.grant('deploy#initial', 'security-model-user', ['Environments/security-model-dir'])

switchUser('security-model-user')
repository.read(env.id)

switchUser('admin')

security.revoke('deploy#upgrade', 'security-model-user', ['Environments/security-model-dir'])

switchUser('security-model-user')
repository.read(env.id)

switchUser('admin')
security.revoke('deploy#initial', 'security-model-user', ['Environments/security-model-dir'])
