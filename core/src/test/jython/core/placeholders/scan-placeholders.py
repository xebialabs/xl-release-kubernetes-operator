from java.io import File
from com.xebialabs.deployit.integration.test.support import TFiles
from java.lang import System

tmpDir = str(System.getProperty("java.io.tmpdir"))
dict = create_random_dict({'entries':{'NAME':'tar','DB_USERNAME':'test','COM':'xebialabs'}})
server = create_random_yak_server()
env = create_random_environment("scan-placeholders", [server.id], [dict.id])

# Generating Deployeds
depl = deployment.prepareInitial("Applications/PlaceholderApp3/1.0", env.id)
depl = deployment.prepareAutoDeployeds(depl)

assertNotNone(depl.deployeds)
assertEquals(7, len(depl.deployeds))

for archive in depl.deployeds:
    print "Preparing archive", archive.name
    archive.tempFile = tmpDir + File.separator + archive.name

taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)

for archive in depl.deployeds:
    print "Asserting archive", archive.tempFile
    lines = TFiles.readLines(archive.tempFile + "/placeholders.txt")
    assertEquals("My username is test", lines.get(0))
    assertEquals("My password is test", lines.get(1))
    assertEquals("My name is tar", lines.get(2))
    assertEquals("My companyName is xebialabs", lines.get(3))
    lines = TFiles.readLines(archive.tempFile + "/placeholders-utf16le.txt", "UTF-16")
    assertEquals("My username is test", lines.get(0))
    assertEquals("My password is test", lines.get(1))
    assertEquals("My name is tar", lines.get(2))
    assertEquals("My companyName is xebialabs", lines.get(3))
    lines = TFiles.readLines(archive.tempFile + "/placeholders-utf16be.txt", "UTF-16")
    assertEquals("My username is test", lines.get(0))
    assertEquals("My password is test", lines.get(1))
    assertEquals("My name is tar", lines.get(2))
    assertEquals("My companyName is xebialabs", lines.get(3))
    File(archive.tempFile).delete()
