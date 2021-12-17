def createVaultServer(serverName):
    return repository.create(factory.configurationItem('Configuration/' + serverName, 'secrets.hashicorp.vault.Server',{'name': serverName, 'serverAddress': 'http://127.0.0.1:8210', 'token': 'myroot'}))

def createSecretEngine(serverName, engineName, path, version):
    return repository.create(factory.configurationItem(serverName + '/' + engineName, 'secrets.hashicorp.vault.SecretEngine',{'path': path, 'kvBackendVersion': version}))

def createVaultEnvironment(environmentId, containers, dictionaries):
    return repository.create(factory.configurationItem("Environments/" + environmentId, "udm.Environment", {'members':map(lambda c: c.id, containers), 'dictionaries': map(lambda d: d.id, dictionaries)}))

def createVaultDictionary(dictName, secretPaths):
    return repository.create(factory.configurationItem('Environments/' + dictName, 'secrets.hashicorp.vault.Dictionary', {'vaultServer': 'Configuration/Vault', 'secretPaths': secretPaths}))
