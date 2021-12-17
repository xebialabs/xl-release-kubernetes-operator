from com.xebialabs.deployit.plugin.api.validation import ValidationMessage

vaultServer = createVaultServer('VaultServer-noConnection')
vaultServer.serverAddress = 'http://127.0.0.1:28201'
repository.update(vaultServer)
provider = repository.create(factory.configurationItem(
    'Configuration/LookupProvider-vaultlookuptestnocon','secrets.hashicorp.vault.LookupValueProvider',
    {'vaultServer' : vaultServer.id,'secretPaths':['secret/hello']}))
host = repository.create(factory.configurationItem(
    'Infrastructure/Host-Lookup-vaultlookuptestnocon','overthere.SshHost',
    {'os':'unix', 'address':'somewhere', 'username':'somename'}))

try:
    # The password is not set on the host
    host = repository.read('Infrastructure/Host-Lookup-vaultlookuptestnocon')
    assertNone(host.password)

    # with wrong key and wrong type
    host.lookup["password"] = provider, "HOST_PASSWD"
    host.lookup["port"] = provider, "HOST_PASSWD"
    host = repository.update(host)

    validationMessages = sorted(host.validations, key=lambda x: x.propertyName)

    assertEquals(2, len(validationMessages))

    assertEquals(ValidationMessage.Level.WARNING, validationMessages[0].level)
    assertEquals('Infrastructure/Host-Lookup-vaultlookuptestnocon', validationMessages[0].ciId)
    assertEquals('password', validationMessages[0].propertyName)
    assertTrue(
        'cannot be accessed to resolve value for field' in validationMessages[0].message
        and 'password' in validationMessages[0].message
        and 'Configuration/LookupProvider-vaultlookuptestnocon' in validationMessages[0].message,
        "Test failed: validation message should contain:" +
        " 'cannot be accessed to resolve value for field', 'password' and 'Configuration/LookupProvider-vaultlookuptestnocon' but message was '"
        +  validationMessages[0].message + "'")

    assertEquals(ValidationMessage.Level.WARNING, validationMessages[1].level)
    assertEquals('Infrastructure/Host-Lookup-vaultlookuptestnocon', validationMessages[1].ciId)
    assertEquals('port', validationMessages[1].propertyName)
    assertTrue(
        'cannot be accessed to resolve value for field' in validationMessages[1].message
        and 'port' in validationMessages[1].message
        and 'Configuration/LookupProvider-vaultlookuptestnocon' in validationMessages[1].message,
        "Test failed: validation message should contain:" +
        " 'cannot be accessed to resolve value for field', 'port' and 'Configuration/LookupProvider-vaultlookuptestnocon' but message was '"
        +  validationMessages[1].message + "'")


finally:
    repository.delete(host.id)
    repository.delete(provider.id)
    repository.delete(vaultServer.id)
