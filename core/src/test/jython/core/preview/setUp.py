groupName = "preview-block"

previewApp = repository.create(factory.configurationItem('Applications/preview-YakApp','udm.Application',{}))
yakPackage10 = repository.create(factory.configurationItem(previewApp.id + "/10.0", "udm.DeploymentPackage"))
repository.create(factory.configurationItem(yakPackage10.id + "/scriptSpec", "yak.YakPreviewSpec"))
srv1 = repository.create(factory.configurationItem("Infrastructure/%s-srv1" % groupName, "yak.YakServer", {}))
srv2 = repository.create(factory.configurationItem("Infrastructure/%s-srv2" % groupName, "yak.YakServer", {}))
envDirectory = repository.create(factory.configurationItem("Environments/%s" % groupName, "core.Directory"))
multiServerEnv = repository.create(factory.configurationItem("%s/env2" % envDirectory.id, "udm.Environment", {"members": [srv1.id, srv2.id]}))

