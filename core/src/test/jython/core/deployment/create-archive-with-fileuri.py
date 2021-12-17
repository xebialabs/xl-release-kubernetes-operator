from com.xebialabs.restito.builder.stub.StubHttp import *
from com.xebialabs.restito.semantics.Action import *
from com.xebialabs.restito.semantics.Condition import *
from com.xebialabs.restito.server import StubServer
import socket

app = create_random_application('MyApplication')
assertTrue(repository.exists(app.id))

app1_0 = repository.create(factory.configurationItem('%s/1.0' % app.id, 'udm.DeploymentPackage'))
assertTrue(repository.exists(app1_0.id))

server = None
try:
    server = StubServer([]).run()
    whenHttp(server).match(get("/placeholders.txt")).then(stringContent("Some content within the file"))

    archive001 = factory.configurationItem('%s/archive001' % app1_0.id, 'file.Archive',
                                           {"fileUri": "http://%s:%s/placeholders.txt" % (socket.gethostname(), str(server.getPort()))})
    app1_0_archive = repository.create(archive001)
    assertTrue(repository.exists(app1_0_archive.id))

    archive002 = factory.configurationItem('%s/archive002' % app1_0.id, 'file.Archive',
                                           {"fileUri": "http://%s:%s/placeholders.txt" % (socket.gethostname(),str(server.getPort()))})
    archive003 = factory.configurationItem('%s/archive003' % app1_0.id, 'file.Archive',
                                           {"fileUri": "http://%s:%s/placeholders.txt" % (socket.gethostname(), str(server.getPort()))})
    portalWar = factory.configurationItem('%s/PortalWar' % app1_0.id, 'test-v3.PortalWar')

    app1_0_mixed_cis = repository.create([archive002, archive003, portalWar])

    assertTrue(repository.exists(app1_0_mixed_cis[0].id))
    assertTrue(repository.exists(app1_0_mixed_cis[1].id))
    assertTrue(repository.exists(app1_0_mixed_cis[2].id))

finally:
    if server:
        server.stop()
