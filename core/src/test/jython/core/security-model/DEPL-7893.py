# repo-test-user

repository.create(factory.configurationItem('Infrastructure/repo-dir','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/repo-non-read','core.Directory',{}))
security.createUser('repo-test-user', DEFAULT_PASSWORD)
security.assignRole('repo-test-user', ['repo-test-user'])
security.grant('login', 'repo-test-user')
security.grant('repo#edit', 'repo-test-user', ['Infrastructure/repo-dir'])
security.grant('read', 'repo-test-user', ['Infrastructure/repo-dir'])

ci = repository.create(factory.configurationItem('Infrastructure/repo-dir/repo-readable-host', 'overthere.LocalHost', {"os": os_family()}))

security.logout()
security.login("repo-test-user", DEFAULT_PASSWORD)

should_fail("Cannot move to non-read directory", repository.move, ci, 'Infrastructure/repo-non-read/repo-readable-host')

security.logout()
security.login("admin", "admin")

should_fail("Should not have moved", repository.read, 'Infrastructure/repo-non-read/repo-readable-host')

security.deleteUser("repo-test-user")
security.revoke('login', 'repo-test-user')
security.revoke('repo#edit', 'repo-test-user', ['Infrastructure/repo-dir'])
security.revoke('read', 'repo-test-user', ['Infrastructure/repo-dir'])
security.removeRole('repo-test-user')

repository.delete('Infrastructure/repo-dir')
repository.delete('Infrastructure/repo-non-read')

