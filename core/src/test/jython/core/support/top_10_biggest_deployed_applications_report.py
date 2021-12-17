from test import TestUtils
from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from org.apache.commons.io import FileUtils
from java.io import File
import json

support = proxies.support

tempDir = TemporaryDirectoryHolder.getTemporaryDirectory()
zipFile = File(tempDir, "xld-support-package.zip")

try:

    # do one deployment
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

    # get zip content
    result = support.generateSupportZip()

    # read zip file from server
    resultStream = result.entity
    FileUtils.copyInputStreamToFile(resultStream, zipFile)
    resultStream.close()
    assertTrue(zipFile.exists())

    # check report json
    top10BiggestDeployedApplicationsResult = TestUtils.readFromZip(zipFile.absolutePath, "Top10BiggestDeployedApplicationsInYear.json")
    assertNotEquals("[]", top10BiggestDeployedApplicationsResult)
    top10BiggestDeployedApplicationsJson = json.loads(top10BiggestDeployedApplicationsResult)
    assertTrue(len(top10BiggestDeployedApplicationsJson) > 0, "Expecting " + str(len(top10BiggestDeployedApplicationsJson)) + " to be grater then 0")

finally:
    zipFile.delete()
