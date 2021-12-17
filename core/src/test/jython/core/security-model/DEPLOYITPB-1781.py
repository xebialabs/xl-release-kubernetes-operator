group = repository.create(factory.configurationItem('Infrastructure/issues-group','core.Directory', {}))
host = factory.configurationItem('Infrastructure/issues-group/issues-myServer', "test-v3.DummyHost", {'accessMethod':'SSH_SFTP','os':'UNIX','address':'myServer', 'username':'foo', 'password':'bar'})
repository.create(host)

result = repository.search('test-v3.DummyHost')
assertTrue(host.id in result)

devUser = security.createUser("issues-user-test", DEFAULT_PASSWORD)
security.assignRole('issues-user-test', ['issues-user-test'])

security.grant("login", "issues-user-test")

security.logout()
security.login('issues-user-test', DEFAULT_PASSWORD)

result = repository.search('test-v3.DummyHost')
assertFalse(host.id in result)

security.logout()
security.login('admin', 'admin')
security.grant("read", "issues-user-test",[group.id])

security.logout()
security.login('issues-user-test', DEFAULT_PASSWORD)
result = repository.search('test-v3.DummyHost')
assertTrue(host.id in result)

security.logout()
security.login('admin', 'admin')
security.revoke("read", "issues-user-test",[group.id])

security.logout()
security.login('issues-user-test', DEFAULT_PASSWORD)
result = repository.search('test-v3.DummyHost')
assertFalse(host.id in result)

security.logout()
security.login('admin', 'admin')

repository.delete(host.id)
security.revoke("login", "issues-user-test")

security.removeRole('issues-user-test')

security.deleteUser('issues-user-test')

repository.delete(group.id)