envDir = repository.create(factory.configurationItem('Environments/issues-dir1','core.Directory',{}))
appDir = repository.create(factory.configurationItem('Applications/issues-dir1','core.Directory',{}))
envDir2 = repository.create(factory.configurationItem('Environments/issues-dir2','core.Directory',{}))

app = repository.create(factory.configurationItem('Applications/issues-dir1/issues-tinyApp', 'udm.Application', {}))
host = repository.create(factory.configurationItem('Infrastructure/issues-host', 'yak.YakServer'))
env0 = repository.create(factory.configurationItem('Environments/issues-dir1/issues-0hostEnv0', 'udm.Environment', {'members':[host.id]}))
env1 = repository.create(factory.configurationItem('Environments/issues-dir2/issues-1tinyEnv1', 'udm.Environment', {'members':[host.id]}))
env2 = repository.create(factory.configurationItem('Environments/issues-dir2/issues-2tinyEnv2', 'udm.Environment', {'members':[host.id]}))

security.createUser("issues-user-richard", DEFAULT_PASSWORD)
security.assignRole('issues-user-richard', ['issues-user-richard'])

security.grant("login", "issues-user-richard")
security.grant("read", "issues-user-richard", [ appDir.id ])
security.grant("deploy#upgrade", "issues-user-richard", [ envDir.id ])
security.logout()
security.login("issues-user-richard", DEFAULT_PASSWORD)
assertEquals(1, len(repository.search('udm.Application')))
assertEquals(1, len(repository.search('udm.Environment')))

security.logout()
security.login('admin', 'admin')

security.grant('read', 'issues-user-richard', [envDir2.id])

security.logout()
security.login('issues-user-richard', DEFAULT_PASSWORD)

assertEquals(3, len(repository.search('udm.Environment')))
repository.read(env1.id)

security.logout()
security.login('admin', 'admin')

security.revoke('read', 'issues-user-richard', [envDir2.id])
security.revoke("read", "issues-user-richard", [ appDir.id ])
security.revoke("deploy#upgrade", "issues-user-richard", [ envDir.id ])
security.revoke("login", "issues-user-richard")
security.removeRole('issues-user-richard')
repository.delete(appDir.id)
repository.delete(envDir.id)
repository.delete(envDir2.id)
repository.delete(host.id)
security.deleteUser('issues-user-richard')