newHost = repository.create(factory.configurationItem("Infrastructure/security-model-dir/host", "test-v3.DummyJeeServer", {'hostName':'localhost'}))
security.assignRole('security-model-mallory', [])
switchUser('security-model-user')

assertFalse(security.hasPermission('read', 'Infrastructure/security-model-dir/host'))

switchUser('admin')
security.grant('read', 'security-model-user', ['Infrastructure'])

switchUser('security-model-user')

assertTrue(security.hasPermission('read', 'Infrastructure/security-model-dir/host'))

switchUser('admin')

security.grant('repo#edit', 'security-model-mallory', ['Infrastructure/security-model-dir'])

switchUser('security-model-user')

assertFalse(security.hasPermission('read', 'Infrastructure/security-model-dir/host'))

switchUser('admin')
security.revoke('read', 'security-model-user', ['Infrastructure'])
security.revoke('repo#edit', 'security-model-mallory', ['Infrastructure/security-model-dir'])
security.removeRole('security-model-mallory')