newHost = repository.create(factory.configurationItem("Infrastructure/security-model-dir/host", "test-v3.DummyJeeServer", {'hostName':'localhost'}))
security.grant('read', 'security-model-user', ['Infrastructure'])
security.grant('read', 'security-model-user', ['Infrastructure/security-model-dir'])
try:
	security.grant('read', 'security-model-user', ['Infrastructure/security-model-dir/host'])
except:
	print('ok')
else:
	raise Exception("Can only grant on directory and root")

security.revoke('read', 'security-model-user', ['Infrastructure/security-model-dir'])
security.revoke('read', 'security-model-user', ['Infrastructure'])
repository.delete(newHost.id)