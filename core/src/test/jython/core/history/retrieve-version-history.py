switchUser('alice-history')
host = create_random_server('version-history-host', 'test-v3.DummyHost', {'address':'localhost','os':'UNIX','accessMethod':'local','username':'root','password':'root'})

switchUser('bob-history')
host.username = 'admin'
host = repository.update(host)

switchUser('mallory-history')
host.password = 'foobar'
repository.update(host)

revisions = repository.getVersionHistory(host.id)
assertEquals(3, len(revisions))

assertEquals('alice-history',revisions[0].username)
assertEquals('bob-history',revisions[1].username)
assertEquals('current',revisions[2].revisionName)
assertEquals('mallory-history',revisions[2].username)
