from test import TestUtils
from com.xebialabs.deployit.core.util import CiUtils

folder = create_random_folder("exportcis-folder")
app = create_random_application("%s/exportcis-ExportApp" % CiUtils.getName(folder.id))
myAppPackageId = createPackage(app.id).id
createFile(myAppPackageId, "file-1", "my-file.txt", "Test content")

myAppWithFolder = create_random_application("%s/exportcis-ExportAppWithFolder" % CiUtils.getName(folder.id))
myAppWithFolderPackageId = createPackage(myAppWithFolder.id).id
createFolder(myAppWithFolderPackageId, "folder-1", "my-folder.zip")

host = create_random_host("exportcis-exporthost")
env = create_random_environment("exportcis-exportEnv", [host.id])

depl = deployment.prepareInitial(myAppWithFolderPackageId, env.id)
depl = deployment.prepareAutoDeployeds(depl)
deployit.startTaskAndWait(deployment.createDeployTask(depl).id)

taskId = repository.exportCis(folder.id)
assertNotNone(taskId)

exportTargetFile = os.path.join(_integration_server_runtime_directory, task2.get(taskId).metadata['exportedFile'])
assertNotNone(exportTargetFile)

deployit.startTaskAndWait(taskId)

assertTrue(os.path.exists(exportTargetFile))

xml_content = TestUtils.readFromZip(exportTargetFile, 'configuration-items.xml')
parse_xml_content(xml_content)

file_content = TestUtils.readFromZip(exportTargetFile, '%s/file-1/my-file.txt' % myAppPackageId)
assertEquals("Test content", file_content)
