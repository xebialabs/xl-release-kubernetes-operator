
server = repository.create(factory.configurationItem("Infrastructure/repo-dummy1", "test-v3.DummyJeeServer", {'hostName':'localhost', 'password':'obfuscated'}))
comparison1 = deployit.compare(server.id, [])
server2 = repository.create(factory.configurationItem("Infrastructure/repo-dummy2", "test-v3.DummyJeeServer", {'hostName':'http://www.google.com', 'password':'obfuscated'}))
comparison2 = deployit.compare(server.id, [server2.id])
for line in comparison2.lines:
    if line.key == "hostName":
        assertEquals("localhost", line.referenceValue)
        assertEquals("http://www.google.com", line.values[0])

repository.delete(server.id)
repository.delete(server2.id)