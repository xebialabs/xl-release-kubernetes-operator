repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp','udm.Application',{}))

deployit.importPackage('SecurityModelApp/1.0')
switchUser('security-model-user')

ids = repository.search(None, 'Applications')
assertEquals(0, len(ids))

switchUser('admin')
security.grant('read', 'security-model-user', ['Applications/security-model-dir'])
switchUser('security-model-user')

ids = repository.search(None, 'Applications')
assertEquals(1, len(ids))

switchUser('admin')
security.revoke('read', 'security-model-user', ['Applications/security-model-dir'])