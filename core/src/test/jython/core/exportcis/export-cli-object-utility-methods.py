from test import TestUtils
from com.xebialabs.deployit.core.util import CiUtils

folder = create_random_folder("exportcis-folder", "Infrastructure")
host = createHost("exportcis-exporthost", CiUtils.getName(folder.id))

exportTargetFile = os.path.join(_integration_server_runtime_directory, repository.exportCisAndWait(folder.id))

assertNotNone(exportTargetFile)
assertTrue(os.path.exists(exportTargetFile))

parse_xml_content(TestUtils.readFromZip(exportTargetFile, 'configuration-items.xml'))
