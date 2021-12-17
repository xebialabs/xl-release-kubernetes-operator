security.createUser('security-model-user', DEFAULT_PASSWORD)
security.assignRole('security-model-user', ['security-model-user'])
security.grant('login', 'security-model-user')

repository.create(factory.configurationItem('Applications/security-model-dir','core.Directory',{}))
repository.create(factory.configurationItem('Environments/security-model-dir','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/security-model-dir','core.Directory',{}))
