from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from os.path import isfile, join

filename = "IssuesApp1-1.0.dar"
zip_name = "hello.zip"
importedpackage = "src/test/resources/packages/issues/" + filename

# defining a temporary folder
workdir = TemporaryDirectoryHolder.getTemporaryDirectory().path

# import the package into the repo
package = deployit.importPackage(importedpackage)

# exporting the package from the repo
repository.exportDar(workdir, "Applications/IssuesApp1/1.0")

# creating a manifest from imported dar file
exportzip = ZipFile(join(workdir, filename))
zip_export = ZipFile(exportzip.extract(exportzip.getinfo("hello/hello.zip"), workdir))

assertTrue(zip_export.getinfo("hello.txt").external_attr != 0)

# cleaning up
repository.delete('Applications/IssuesApp1')
