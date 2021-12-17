dir = repository.create(factory.configurationItem('Environments/issues-dir','core.Directory',{}))

host = repository.create(factory.configurationItem('Infrastructure/issues-myServer',"yak.YakServer", {}))
myEnv = repository.create(factory.configurationItem('Environments/issues-dir/issues-myEnv' , "udm.Environment", {'members':[host.id]}))

myDict = repository.create(factory.configurationItem('Environments/issues-myDict',"udm.Dictionary", {}))
host2 = repository.create(factory.configurationItem('Infrastructure/issues-myServer2',"yak.YakServer", {}))
myEnv2 = repository.create(factory.configurationItem('Environments/issues-dir/issues-myEnv2' , "udm.Environment", {'members':[host2.id],'dictionaries':[myDict.id]}))

hostResult = repository.search('yak.YakServer')
assert host.id in hostResult
assert host2.id in hostResult

devUser = security.createUser("issues-user-developer", DEFAULT_PASSWORD)
security.assignRole('issues-user-developer', ['issues-user-developer'])
security.grant("login", "issues-user-developer")
security.grant("deploy#initial", "issues-user-developer", [dir.id])
security.grant("deploy#upgrade", "issues-user-developer", [dir.id])

security.logout()
security.login('issues-user-developer', DEFAULT_PASSWORD)

envResult = repository.search('udm.Environment')
assert myEnv.id in envResult
assert myEnv2.id in envResult

assertNotNone(repository.read(myEnv.id))

hostResult = repository.search('yak.YakServer')
assert host.id not in hostResult
assert host2.id not in hostResult

security.logout()
security.login('admin', 'admin')

security.revoke("login", "issues-user-developer")
security.revoke("deploy#initial", "issues-user-developer", [dir.id])
security.revoke("deploy#upgrade", "issues-user-developer", [dir.id])

security.deleteUser('issues-user-developer')
security.removeRole('issues-user-developer')
repository.delete(dir.id)
repository.delete(host.id)
repository.delete(host2.id)
repository.delete(myDict.id)

