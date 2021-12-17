from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.base import Charsets
from com.google.common.io import Files

dict = create_random_dict({'entries':{'bar':'<ignore>'}})
encryptedDict = create_random_dict({'entries':{'foo':'John Reese'}}, 'udm.EncryptedDictionary')
server1 = create_random_yak_server()
env1 = create_random_environment("encrypted-dict-deployment", [server1.id], [dict.id, encryptedDict.id])

package = repository.read("Applications/PlaceholderApp/3.0")

depl = deployment.prepareInitial(package.id, env1.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)
assertEquals(1, len(depl.deployeds))
file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployedPlaceholders5.yak")
depl.deployeds[0].tempFile = file.path
assertNotEquals(depl.deployeds[0].placeholders['foo'],'John Reese')
if (not depl.deployeds[0].placeholders['foo'].startswith('e{{aes')):
	raise Exception("should be encrypted")

assertEquals('<ignore>', depl.deployeds[0].placeholders['bar'])

taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

assertTrue(file.exists())
lines = Files.readLines(file, Charsets.UTF_8)

assertEquals("My name is John Reese", lines[0])
assertEquals("I work in {{bar}}", lines[1])

file.delete()
