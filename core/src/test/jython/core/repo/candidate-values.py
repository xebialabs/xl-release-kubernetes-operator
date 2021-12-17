host1 = repository.create(factory.configurationItem('Infrastructure/repo-host1', "test-v3.DummyHost", {'accessMethod':'SSH_SFTP','os':'UNIX','address':'myServer', 'username':'foo', 'password':'bar'}))
server1 = repository.create(factory.configurationItem('Infrastructure/repo-host1/repo-server1', 'test-v3.DummyJeeServerOnDummyHost'))
host2 = repository.create(factory.configurationItem('Infrastructure/repo-host2', "test-v3.DummyHost", {'accessMethod':'SSH_SFTP','os':'UNIX','address':'myServer', 'username':'foo', 'password':'bar'}))
server2 = repository.create(factory.configurationItem('Infrastructure/repo-host2/repo-server2', 'test-v3.DummyJeeServerOnDummyHost'))
jdbc1 = repository.create(factory.configurationItem('Infrastructure/repo-host1/repo-server1/repo-jdbc1', 'test-v3.DummyJeeServerOnDummyHostDeployedJdbcProvider'))
jdbc2 = repository.create(factory.configurationItem('Infrastructure/repo-host2/repo-server2/repo-jdbc2', 'test-v3.DummyJeeServerOnDummyHostDeployedJdbcProvider'))

ds = factory.configurationItem('Infrastructure/repo-host1/repo-server1/ds', 'test-v3.DummyJeeServerOnDummyHostDeployedDatasource', {'container': 'Infrastructure/repo-host1/repo-server1'})

candidates = proxies.repository.candidateValues('unfilteredJdbc', None, None, 0, 0, ds._ci)
assertEquals(2, len(candidates))

candidates = proxies.repository.candidateValues('filteredJdbc', None, None, 0, 0, ds._ci)
assertEquals(1, len(candidates))


repository.delete(host2.id)
repository.delete(host1.id)
