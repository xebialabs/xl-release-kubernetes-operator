from com.xebialabs.restito.builder.stub.StubHttp import *
from com.xebialabs.restito.semantics.Action import *
from com.xebialabs.restito.semantics.Condition import *
from com.xebialabs.restito.server import StubServer
import socket

content = "This is {{foo}} and the other guy is {{bar}}"
server = StubServer([]).run()
whenHttp(server).match(get("/placeholders.txt")).then(stringContent(content))

app = create_random_application("embedded_artifact_EmbeddedArtifactApp")
embeddedArtifactAppPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % app.id, 'udm.DeploymentPackage', {}))
embeddedArtifactDeployable = repository.create(factory.configurationItem('%s/embeddedDeployable' % embeddedArtifactAppPackage_1_0.id, 'test.ParentDeployable', {}))

ci = factory.configurationItem('%s/zipArtifact' % embeddedArtifactDeployable.id, 'test.ChildEmbeddedDeployable', {'fileUri':"http://%s:%s/placeholders.txt" % (socket.gethostname(), str(server.getPort()))})

created = repository.create(ci)

expectedPlaceholders = ["foo", "bar"]

assertEquals(2, len(created.placeholders))

for ph in created.placeholders:
    if not ph in expectedPlaceholders:
        fail("Did not find placeholder %s in %s" % (ph, str(created.placeholders)))

import hashlib
assertEquals(hashlib.sha256(content).hexdigest(), created.checksum)

server.stop()
