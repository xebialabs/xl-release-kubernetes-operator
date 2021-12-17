from com.xebialabs.restito.builder.stub.StubHttp import *
from com.xebialabs.restito.semantics.Action import *
from com.xebialabs.restito.semantics.Condition import *
from com.xebialabs.restito.server import StubServer
import socket

content = "{{ key }}"
server = StubServer([]).run()
whenHttp(server).match(get("/placeholders2.txt")).then(stringContent(content))

# Prepare applications
deployedsApp = create_random_application('pkg-with-placeholders-AppToScanPlaceholders')

# Prepare packages
createApp1_0 = repository.create(factory.configurationItem(
    '%s/1.0' % deployedsApp.id,
    'udm.DeploymentPackage',
    {'dependencyResolution': '{{createResolution}}'}
))

updateApp2_0 = repository.create(factory.configurationItem(
    '%s/2.0' % deployedsApp.id,
    'udm.DeploymentPackage',
    {'dependencyResolution': '{{updateResolution}}'}
))

fileWithPlaceholders = repository.create(factory.configurationItem(
    '%s/File-{{updateName}}' % updateApp2_0.id,
    'file.File',
    {'fileUri':"http://%s:%s/placeholders2.txt" % (socket.gethostname(), str(server.getPort())),
     'targetPath': '{{targetNew}}'}
))

renameApp3_0 = repository.create(factory.configurationItem(
    '%s/3.0' % deployedsApp.id,
    'udm.DeploymentPackage',
    {'dependencyResolution': '{{renameResolution}}'}
))

deleteApp4_0 = repository.create(factory.configurationItem(
    '%s/4.0' % deployedsApp.id,
    'udm.DeploymentPackage',
    {'dependencyResolution': '{{deleteResolution}}'}
))

# Request defined placeholders for key
placeholders_createResolution = placeholder.definedPlaceholders("createResolution")
placeholders_updateResolution = placeholder.definedPlaceholders("updateResolution")
placeholders_renameResolution = placeholder.definedPlaceholders("renameResolution")
placeholders_deleteResolution = placeholder.definedPlaceholders("deleteResolution")

# Assert
assertEquals(1, len(placeholders_createResolution))

assertEquals('createResolution', placeholders_createResolution[0].key)
assertEquals('%s/1.0' % deployedsApp.id, placeholders_createResolution[0].ciId)
assertEquals('udm.DeploymentPackage', placeholders_createResolution[0].ciType)

assertEquals(1, len(placeholders_updateResolution))

assertEquals('updateResolution', placeholders_updateResolution[0].key)
assertEquals('%s/2.0' % deployedsApp.id, placeholders_updateResolution[0].ciId)
assertEquals('udm.DeploymentPackage', placeholders_updateResolution[0].ciType)

assertEquals(1, len(placeholders_renameResolution))

assertEquals('renameResolution', placeholders_renameResolution[0].key)
assertEquals('%s/3.0' % deployedsApp.id, placeholders_renameResolution[0].ciId)
assertEquals('udm.DeploymentPackage', placeholders_renameResolution[0].ciType)

assertEquals(1, len(placeholders_deleteResolution))

assertEquals('deleteResolution', placeholders_deleteResolution[0].key)
assertEquals('%s/4.0' % deployedsApp.id, placeholders_deleteResolution[0].ciId)
assertEquals('udm.DeploymentPackage', placeholders_deleteResolution[0].ciType)
