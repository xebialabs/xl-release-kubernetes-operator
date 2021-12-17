import tempfile
import os

filename = "EmptyPackage-1.0.dar"
importedpackage = 'EmptyPackage/1.0'

# defining a temporary folder
workdir = tempfile.mkdtemp()

# import the package into the repo
package = deployit.importPackage(importedpackage)

assertTrue(repository.exists(package.id))

# exporting the package from the repo
repository.exportDar(workdir, package.id)

# creating a manifest from imported dar file
exportzip = ZipFile(workdir + os.path.sep + filename)
bytesexport = exportzip.read("deployit-manifest.xml")

assertNotEquals(bytesexport.find("<deployables />"), -1)

#cleaning up
repository.delete('Applications/EmptyPackage')
