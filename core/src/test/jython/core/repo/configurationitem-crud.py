from java.text import SimpleDateFormat
from java.util import Calendar

# create configuration item
initialHost = factory.configurationItem("Infrastructure/repo-testConfigurationItem", "test-v3.DummyJeeServer", {'hostName':'localhost', 'password':'obfuscated'})
actualCreatedHost = repository.create(initialHost)
assertEquals("repo-testConfigurationItem", actualCreatedHost.name)

# list configuration items
existingCis = repository.search("test-v3.DummyJeeServer")
assertNotNone(existingCis)

# read configuration item
assertNotNone(actualCreatedHost)
assertEquals("test-v3.DummyJeeServer", actualCreatedHost.type)
assertEquals("localhost", actualCreatedHost.hostName)
assertNotEquals("obfuscated", actualCreatedHost.password)

# update configuration item
updatedHost = factory.configurationItem(actualCreatedHost.id, "test-v3.DummyJeeServer", {'hostName':'google', 'password':'somethingels'})
actualUpdatedHost = repository.update(updatedHost)

assertEquals("test-v3.DummyJeeServer", actualUpdatedHost.type)
assertEquals("google", actualUpdatedHost.hostName)

# delete configuration item
repository.delete(actualUpdatedHost.id)
