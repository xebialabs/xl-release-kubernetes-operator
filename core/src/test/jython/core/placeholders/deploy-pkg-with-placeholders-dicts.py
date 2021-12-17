from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.base import Charsets
from com.google.common.io import Files

dict = create_random_dict({'entries':{'foo':'<empty>','bar':'<ignore>'}})
server = create_random_yak_server()
env = create_random_environment('pkg-with-placeholders', [server.id], [dict.id])

depl = deployment.prepareInitial("Applications/PlaceholderApp/3.0", env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)
assertEquals(1, len(depl.deployeds))
file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployedPlaceholders3.yak")
depl.deployeds[0].tempFile = file.path
assertEquals('<empty>', depl.deployeds[0].placeholders['foo'])
assertEquals('<ignore>', depl.deployeds[0].placeholders['bar'])

taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

assertTrue(file.exists())
lines = Files.readLines(file, Charsets.UTF_8)

assertEquals("My name is ", lines[0])
assertEquals("I work in {{bar}}", lines[1])

file.delete()
