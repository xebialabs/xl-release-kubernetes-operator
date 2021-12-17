# repo-user

repoDir = repository.create(factory.configurationItem('Infrastructure/repo-dir','core.Directory',{}))
repoNonReadDir = repository.create(factory.configurationItem('Infrastructure/repo-non-read','core.Directory',{}))

security.createUser('repo-user', DEFAULT_PASSWORD)
security.assignRole('repo-user', ['repo-user'])
security.grant('login', 'repo-user')
security.grant('repo#edit', 'repo-user', ['Infrastructure/repo-dir'])
security.grant('read', 'repo-user', ['Infrastructure/repo-dir'])

repository.create(factory.configurationItem('Infrastructure/repo-non-read/host', 'overthere.LocalHost', {"os": os_family()}))
repository.create(factory.configurationItem('Infrastructure/repo-non-read/another-host', 'overthere.LocalHost', {"os": os_family()}))
repository.create(factory.configurationItem('Infrastructure/repo-dir/readable-host', 'overthere.LocalHost', {"os": os_family()}))

security.logout()
security.login("repo-user", DEFAULT_PASSWORD)

should_fail('Should not read', repository.read, 'Infrastructure/repo-non-read/host')
ci_non_read_link = factory.configurationItem('Infrastructure/repo-dir/yak', 'yak.YakStagingServer', {'host':'Infrastructure/repo-non-read/host'})
should_fail('Should not create single with repo-non-read link', repository.create, ci_non_read_link)
should_fail('Should not create multi with repo-non-read link', repository.create, [ci_non_read_link])
yakServer = repository.create(factory.configurationItem('Infrastructure/repo-dir/yak', 'yak.YakStagingServer', {}))
yakServer.host = 'Infrastructure/repo-non-read/host'
should_fail('Should not update single with new repo-non-read link', repository.update, yakServer)
should_fail('Should not update multi with new repo-non-read link', repository.update, [yakServer])
with_list = factory.configurationItem('Infrastructure/repo-dir/yak2', 'yak.YakMultiInfra', {'hosts':['Infrastructure/repo-non-read/host']})
should_fail('Should not create ci with repo-non-read link in list', repository.create, with_list)

security.logout()
security.login("admin", "admin")

# Update the yakServer with the dependency
yakServer = repository.update(yakServer)
# Create one with a list
yakMultiInfra = repository.create(factory.configurationItem('Infrastructure/repo-dir/yak2', 'yak.YakMultiInfra', {'hosts':['Infrastructure/repo-non-read/host']}))

security.logout()
security.login("repo-user", DEFAULT_PASSWORD)

yakServer.stagingDir = '/tmp'
# Allowed update because link does not change
yakServer = repository.update(yakServer)
yakServer.host = 'Infrastructure/repo-non-read/another-host'
should_fail('Cannot change link to another repo-non-readable host', repository.update, yakServer)
yakServer.host = 'Infrastructure/repo-dir/readable-host'
# Should be allowed to update to readable host
repository.update(yakServer)

# Copy the current list.
hosts = [i for i in yakMultiInfra.hosts]
yakMultiInfra.hosts.add('Infrastructure/repo-non-read/another-host')
should_fail('Cannot add a repo-non-readable ci to existing list', repository.update, yakMultiInfra)
yakMultiInfra.hosts.clear()
# Should be able to add readable host
yakMultiInfra.hosts.addAll(hosts)
yakMultiInfra.hosts.add('Infrastructure/repo-dir/readable-host')
yakMultiInfra = repository.update(yakMultiInfra)
# should be able to clear all hosts
yakMultiInfra.hosts.clear()
repository.update(yakMultiInfra)

security.logout()
security.login("admin", "admin")

security.deleteUser("repo-user")
security.revoke('login', 'repo-user')
security.revoke('repo#edit', 'repo-user', ['Infrastructure/repo-dir'])
security.revoke('read', 'repo-user', ['Infrastructure/repo-dir'])
security.removeRole('repo-user')

repository.delete(repoDir.id)
repository.delete(repoNonReadDir.id)

