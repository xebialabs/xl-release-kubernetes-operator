yakServer = repository.create(factory.configurationItem("Infrastructure/rollback-yak1", "yak.YakServer", {}))
yakDirectory = repository.create(factory.configurationItem("Environments/rollback-dir", "core.Directory"))
yakEnv = repository.create(factory.configurationItem("Environments/rollback-dir/rollback-env2", "udm.Environment", {"members": [yakServer.id]}))


