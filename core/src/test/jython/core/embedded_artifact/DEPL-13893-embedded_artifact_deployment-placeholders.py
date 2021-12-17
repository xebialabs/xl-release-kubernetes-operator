from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.base import Charsets
from com.google.common.io import Files

importedPackage = repository.read("Applications/EmbeddedArtifactsWithPlaceholders/1.0")
embArtFile1 = repository.read("%s/nested/file1" % importedPackage.id)
assertEquals(2, len(embArtFile1.placeholders))
embArtFile2 = repository.read("%s/nested/file2" % importedPackage.id)
assertEquals(1, len(embArtFile2.placeholders))

# Creating infrastructure
myhost = repository.create(factory.configurationItem("Infrastructure/emb-artifact-Host","overthere.LocalHost",{"os" : os_family() }))
yakServer1 = repository.create(factory.configurationItem("Infrastructure/emb-artifact-yakServer","yak.YakServer", {"host": myhost.id }))
env = repository.create(factory.configurationItem("Environments/emb-artifact-yakEnv", "udm.Environment", {"members": [yakServer1.id]}))

depl = deployment.prepareInitial(importedPackage.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

assertNotNone(depl.deployeds)
assertEquals(3, len(depl.deployeds))
file1 = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployed-1.yak")
file2 = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployed-2.yak")

assertEquals(2, len(depl.deployeds[1].placeholders))
depl.deployeds[1].tempFile = file1.path
depl.deployeds[1].placeholders['first.placeholder'] = 'Replaced 1'
depl.deployeds[1].placeholders['SECOND_PLACEHOLDER'] = 'Replaced 2'

assertEquals(1, len(depl.deployeds[2].placeholders))
depl.deployeds[2].tempFile = file2.path
depl.deployeds[2].placeholders['look.at.me'] = 'Replaced 3'

taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)
assertTrue(file1.exists())
lines = Files.readLines(file1, Charsets.UTF_8)

assertEquals("first line with Replaced 1", lines[0])
assertEquals("second line with Replaced 2", lines[1])

assertTrue(file2.exists())
lines = Files.readLines(file2, Charsets.UTF_8)

assertEquals("Line with another placeholder Replaced 3", lines[0])

file1.delete()
file2.delete()

repository.delete(env.id)
repository.delete(yakServer1.id)
repository.delete(myhost.id)
