# this script tests if exporting a imported DAR package results in a semantically equal DAR package,
# by comparing the manifest entries and artifact binary data.
# This test integration tests covers the whole path between importing and exporting DAR files.
# the test package also includes embeddeds

from java.lang.System import getProperty
from java.io import ByteArrayInputStream
from java.util.jar import Manifest

filename = "export-testApp-1.0.dar"
earname = "Sample-1.0.ear"
seperator = getProperty('file.separator')
importedpackage = "src/test/resources/packages/export/" + filename

# defining a temporary folder
localtemp = getProperty('java.io.tmpdir')
if (localtemp.endswith('/') or (localtemp.endswith('\\'))):
    workdir = localtemp + 'export-temp-dir'
else:
    workdir = localtemp + seperator + 'export-temp-dir'
print workdir

# import the package into the repo
package = deployit.importPackage(importedpackage)

# exporting the package from the repo
repository.exportDar(workdir, "Applications/export-testApp/1.0")

# creating a manifest from imported dar file
exportzip = ZipFile(workdir + seperator + filename)
bytesexport = exportzip.read("deployit-manifest.xml")
earexport = exportzip.read("dummyEar/" + earname)

# creating a manifest from exported dar file
importzip = ZipFile(importedpackage)
earimport = importzip.read("dummyEar/" + earname)

# compare data of artifact
assertEquals(earimport, earexport)

#cleaning up
repository.delete('Applications/export-testApp')

