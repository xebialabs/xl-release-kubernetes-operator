from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

ci = create_random_host('discovery-dummyHost', 'test-v3.DummyHost', {'username':'admin',
                                                                     'password':'admin',
                                                                     'address':'localhost',
                                                                     'os' : os_family(),
                                                                     'accessMethod':'SSH'})

taskId = deployit.createDiscoveryTask(ci)
deployit.startTaskAndWait(taskId)
results = deployit.retrieveDiscoveryResults(taskId)

deployit.print(results)

assertEquals(8, len(results))

for res in results:
    if ("DummyJeeQueue3" in res.id):
        res.hostName = "localhost"

try:
    repository.create(results)
except DeployitClientException, ex:
    assertTrue("A Configuration Item with ID already exists" in ex.message)
