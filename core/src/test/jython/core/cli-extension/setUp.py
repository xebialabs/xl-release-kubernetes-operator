cliHost = repository.create(factory.configurationItem('Infrastructure/cli-extension-host', 'yak.YakServer'))
cliEnv = repository.create(factory.configurationItem('Environments/cli-extension-Env', 'udm.Environment', {'members':[cliHost.id]}))
