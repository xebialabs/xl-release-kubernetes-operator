from com.xebialabs.deployit.core.util import CiUtils

folder = create_random_folder("exportcis-folder")
infraFolder = create_random_folder("exportcis-folder", "Infrastructure")

app = create_random_application("%s/exportcis-ExportApp" % CiUtils.getName(folder.id))
myAppPackageId = createPackage(app.id).id
createFile(myAppPackageId, "file-1", "my-file.txt", "Test content")

myAppWithFolder = create_random_application("%s/exportcis-ExportAppWithFolder" % CiUtils.getName(folder.id))
myAppWithFolderPackageId = createPackage(myAppWithFolder.id).id
createFolder(myAppWithFolderPackageId, "folder-1", "my-folder.zip")

host = create_random_host("%s/exportcis-exporthost" % CiUtils.getName(infraFolder.id))
env = create_random_environment("exportcis-exportEnv", [host.id])

depl = deployment.prepareInitial(myAppWithFolderPackageId, env.id)
depl = deployment.prepareAutoDeployeds(depl)
deployit.startTaskAndWait(deployment.createDeployTask(depl).id)

exportedFile = repository.exportCisAndWait(infraFolder.id)

repository.delete(env.id)
repository.delete(host.id)

repository.importCisAndWait(exportedFile)

assertTrue(repository.exists('%s/folder-1' % myAppWithFolderPackageId), '%s/folder-1 does not exist' % myAppWithFolderPackageId)

assertTrue(repository.exists(host.id), '%s does not exist' % host.id)
assertTrue(repository.exists('%s/folder-1' % host.id), '%s/folder-1 does not exist' % host.id)
restoredDeployed = repository.read('%s/folder-1' % host.id)
assertEquals(host.id, restoredDeployed.container)
assertEquals(myAppWithFolderPackageId + '/folder-1', restoredDeployed.deployable)
