from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.base import Charsets
from com.google.common.io import Files

yakServer = repository.create(factory.configurationItem("Infrastructure/placeholders-yak1", "yak.YakServer", {}))
yakDirectory = repository.create(factory.configurationItem("Environments/placeholders-dir", "core.Directory"))
yakEnv = repository.create(factory.configurationItem("Environments/placeholders-dir/placeholders-env2", "udm.Environment", {"members": [yakServer.id]}))
vaultServer = createVaultServer('Vault').id
createSecretEngine(vaultServer, 'SecretEngine', 'secret_v1/', 'UNVERSIONED')

dict = createVaultDictionary('VaultDict', ['secret/hello', 'secret_v1/hello'])
yakEnv.values['dictionaries'] = [dict.id]
repository.update(yakEnv)

package = deployit.importPackage('PlaceholderApp/3.0')

depl = deployment.prepareInitial(package.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)
assertEquals(1, len(depl.deployeds))
file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployedPlaceholders.yak")
depl.deployeds[0].tempFile = file.path
assertTrue('e{{aes:v0}' in depl.deployeds[0].placeholders['foo'])
assertTrue('e{{aes:v0}' in depl.deployeds[0].placeholders['bar'])

taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

assertTrue(file.exists())
lines = Files.readLines(file, Charsets.UTF_8)

assertEquals("My name is XL-Deploy", lines[0])
assertEquals("I work in XebiaLabs", lines[1])

file.delete()

yakEnv = repository.read(yakEnv.id)
yakEnv.values['dictionaries'] = []
repository.update(yakEnv)
repository.delete(dict.id)
