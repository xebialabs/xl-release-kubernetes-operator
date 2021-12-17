from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder

try:
    packageCi = deployit.importPackage('DownloadPackageApp/1.0')
    tempDir = TemporaryDirectoryHolder.getTemporaryDirectory()
    repository.exportDar(tempDir.path, packageCi.id)
    assertEquals(1, len(tempDir.listFiles()))
finally:
    repository.delete('Applications/DownloadPackageApp')
