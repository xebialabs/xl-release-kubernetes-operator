from test import TestUtils
from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from org.apache.commons.io import FileUtils
from java.io import File

support = proxies.support

tempDir = TemporaryDirectoryHolder.getTemporaryDirectory()
zipFile = File(tempDir, "xld-support-package.zip")

try:
    result = support.generateSupportZip()

    # read zip file from server
    resultStream = result.entity
    FileUtils.copyInputStreamToFile(resultStream, zipFile)
    resultStream.close()
    assertTrue(zipFile.exists())

    # check plugin file
    pluginsResult = TestUtils.readFromZip(zipFile.absolutePath, "plugins.txt")
    # assertEquals("readme.txt", pluginsResult)

    # check report jsons
    reportJsonResults = TestUtils.listEntries(zipFile.absolutePath, "Top10BiggestDeployedApplicationsInYear.json")
    assertTrue(reportJsonResults.contains("Top10BiggestDeployedApplicationsInYear.json"))

    # check conf dir
    confResults = TestUtils.listEntries(zipFile.absolutePath, "conf/")
    assertTrue(confResults.contains("conf/deployit-license.lic"))
    assertTrue(confResults.contains("conf/deployit.conf"))
    assertTrue(confResults.contains("conf/logback-access.xml"))
    assertTrue(confResults.contains("conf/logback.xml"))

    centralConfigurationResults = TestUtils.listEntries(zipFile.absolutePath, "centralConfiguration/")
    assertTrue(centralConfigurationResults.contains("centralConfiguration/deploy-client.yaml"))
    assertTrue(centralConfigurationResults.contains("centralConfiguration/deploy-command-whitelist.yaml"))
    assertTrue(centralConfigurationResults.contains("centralConfiguration/deploy-db-anonymizer.yaml"))
    assertTrue(centralConfigurationResults.contains("centralConfiguration/deploy-secret-complexity.yaml"))
    assertTrue(centralConfigurationResults.contains("centralConfiguration/deploy-jmx.yaml"))
    assertTrue(centralConfigurationResults.contains("centralConfiguration/deploy-websockets.yaml"))
    assertTrue(centralConfigurationResults.contains("centralConfiguration/deploy-task.yaml"))
    assertTrue(centralConfigurationResults.contains("centralConfiguration/type-defaults.properties"))

    # check log dir
    logResults = TestUtils.listEntries(zipFile.absolutePath, "log/")
    assertTrue(logResults.contains("log/access.log"))

finally:
    zipFile.delete()
