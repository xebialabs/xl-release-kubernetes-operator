from test import TestUtils
from com.xebialabs.deployit.core.util import CiUtils

folder = create_random_folder("exportcis-folder")
app = create_random_application("%s/app-dependencies-ShopFrontend" % CiUtils.getName(folder.id))
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
exportTargetFile = os.path.join(_integration_server_runtime_directory, task2.get(taskId).metadata['exportedFile'])
deployit.startTaskAndWait(taskId)

assertTrue(os.path.exists(exportTargetFile))

inner_zip_path = '%s/folder-1/my-folder.zip' % myAppWithFolderPackageId
tmpDir = tempfile.mkdtemp()
folder_zip_extracted = os.path.join(tmpDir, 'archive-unzipped.zip')
TestUtils.extractEntry(exportTargetFile, inner_zip_path, folder_zip_extracted)
assertEquals('Hello :-)', TestUtils.readFromZip(folder_zip_extracted, 'tmp/1.txt'))
rmdir(tmpDir)
