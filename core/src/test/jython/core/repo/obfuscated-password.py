aHost = factory.configurationItem("Infrastructure/repo-host1", "test-v3.DummyJeeServer", {'hostName':'localhost', 'password':'obfuscated'})
createdHost = repository.create(aHost)

if createdHost.password == 'obfuscated':
    raise Exception("Password is not obfuscated")

repository.delete(aHost.id)
