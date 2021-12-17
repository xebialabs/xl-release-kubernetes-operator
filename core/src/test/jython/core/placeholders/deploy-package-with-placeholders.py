from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.base import Charsets
from com.google.common.io import Files

env = create_random_environment_with_yak_server()

depl = deployment.prepareInitial("Applications/PlaceholderApp/3.0", env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)
assertEquals(1, len(depl.deployeds))
file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployedPlaceholders1.yak")
depl.deployeds[0].tempFile = file.path
depl.deployeds[0].placeholders['foo'] = 'John Doe'
depl.deployeds[0].placeholders['bar'] = 'a Factory'

taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

assertTrue(file.exists())
lines = Files.readLines(file, Charsets.UTF_8)

assertEquals("My name is John Doe", lines[0])
assertEquals("I work in a Factory", lines[1])

file.delete()
