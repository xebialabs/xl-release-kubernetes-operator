from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from os.path import isfile, join

pkg_name = "folderDotZip-1.0.dar"

pkg = deployit.importPackage(pkg_name)

tmp_dir = TemporaryDirectoryHolder.getTemporaryDirectory().path
repository.exportDar(tmp_dir, "Applications/folderDotZip/1.0")

exported_pkg_path = join(tmp_dir, pkg_name)
assertTrue(isfile(exported_pkg_path))

repository.delete(pkg.id)

deployit.importPackage(exported_pkg_path)

repository.delete('Applications/folderDotZip')

