vaultServer = createVaultServer('VaultServer')
provider = repository.create(factory.configurationItem('Configuration/LookupProvider','secrets.hashicorp.vault.LookupValueProvider',{'vaultServer' : vaultServer.id,'secretPaths':['secret/hello']}))
host = repository.create(factory.configurationItem('Infrastructure/Host-Lookup','overthere.SshHost',{'os':'unix', 'address':'somewhere', 'username':'somename'}))

# The password is not set on the host
host = repository.read('Infrastructure/Host-Lookup')
assertNone(host.password)

# It is configured as a "lookup-value"
host.lookup["password"] = provider, "HOST_PASSWD"
repository.update(host)

# When a control task is created, it is set.
control = deployit.prepareControlTask(host, "checkConnection")
assertNotNone(control.configurationItem.password)
assertNotEquals(control.configurationItem.password, 'supersecretpassword') # encrypted
