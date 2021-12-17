from com.xebialabs.restito.builder.stub.StubHttp import *
from com.xebialabs.restito.semantics.Action import *
from com.xebialabs.restito.semantics.Condition import *
from com.xebialabs.restito.server import StubServer
import socket

content = "This is {{foo}} and the other guy is {{bar}}"
server = StubServer([]).run()
whenHttp(server).match(get("/placeholders.txt")).then(stringContent(content))

myApp = create_random_application("artifacts-RemoteArtifactApp")
package1 = repository.create(factory.configurationItem("%s/1.0" % myApp.id, "udm.DeploymentPackage", {}))

ci = factory.configurationItem('%s/zipArtifact' % package1.id, 'test-v3.DummyFileArtifact', {'fileUri':"http://%s:%s/placeholders.txt" % (socket.gethostname(), str(server.getPort()))})

created = repository.create(ci)

expectedPlaceholders = ["foo","bar"]

assertEquals(2, len(created.placeholders))

for ph in created.placeholders:
    if not ph in expectedPlaceholders:
        fail("Did not find placeholder %s in %s" % (ph, str(created.placeholders)))

import hashlib
assertEquals(hashlib.sha256(content).hexdigest(), created.checksum)

server.stop()
