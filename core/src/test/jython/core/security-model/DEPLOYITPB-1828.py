deployit.importPackage('IssuesApp2/1.0')
dir = repository.create(factory.configurationItem('Applications/issues-dir','core.Directory',{}))
repository.move('Applications/IssuesApp2','Applications/issues-dir/IssuesApp2')

security.createUser("issues-user-test", DEFAULT_PASSWORD)
security.assignRole('issues-user-test', ['issues-user-test'])
security.grant("login", "issues-user-test")
security.grant('read', 'issues-user-test', [dir.id])
security.grant("import#remove", "issues-user-test", [ dir.id ])
security.logout()
security.login("issues-user-test", DEFAULT_PASSWORD)
applications = repository.search('udm.Application')
print 'applications searched: %s' %(applications)
assertEquals(1, len(applications))

repository.delete('Applications/issues-dir/IssuesApp2/1.0')

security.logout()
security.login('admin', 'admin')

repository.delete(dir.id)
security.revoke("login", "issues-user-test")
security.removeRole('issues-user-test')

security.deleteUser('issues-user-test')