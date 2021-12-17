from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.base import Charsets
from com.google.common.io import Files
from com.xebialabs.deployit.core.util import CiUtils

yakServer = create_random_yak_server("placeholders-yak1")
yakDirectory = create_random_folder("placeholders-dir", "Environments")
yakEnv = create_random_environment("%s/placeholders-env2" % CiUtils.getName(yakDirectory.id), [yakServer.id])

conjurServer = createConjurServer('Conjur')
policy = createPolicy(conjurServer.id, 'RootPolicy', 'itest')
dict = createConjurDictionary(policy.id, ['foo', 'bar'])

yakEnv.values['dictionaries'] = [dict.id]
repository.update(yakEnv)

depl = deployment.prepareInitial("Applications/PlaceholderApp/4.0", yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)
assertEquals(1, len(depl.deployeds))
file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployedPlaceholders.yak")
depl.deployeds[0].tempFile = file.path
print depl.deployeds[0].placeholders
assertTrue('e{{aes:v0}' in depl.deployeds[0].placeholders['foo'])
assertTrue('e{{aes:v0}' in depl.deployeds[0].placeholders['bar'])

taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

assertTrue(file.exists())
lines = Files.readLines(file, Charsets.UTF_8)
assertEquals("My name is XL-Deploy", lines[0])
assertEquals("I work in XebiaLabs", lines[1])

file.delete()
