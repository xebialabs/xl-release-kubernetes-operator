from com.xebialabs.deployit.plugin.api.validation import ValidationMessage

vaultServer = createVaultServer('VaultServer-validation')
provider = repository.create(factory.configurationItem(
    'Configuration/LookupProvider-vaultlookuptest','secrets.hashicorp.vault.LookupValueProvider',
    {'vaultServer' : vaultServer.id,'secretPaths':['secret/hello']}))
host = repository.create(factory.configurationItem(
    'Infrastructure/Host-Lookup-vaultlookuptest','overthere.SshHost',
    {'os':'unix', 'address':'somewhere', 'username':'somename'}))

try:
    # The password is not set on the host
    host = repository.read('Infrastructure/Host-Lookup-vaultlookuptest')
    assertNone(host.password)

    # with wrong key and wrong type
    host.lookup["password"] = provider, "WRONG_KEY"
    host.lookup["port"] = provider, "HOST_PASSWD"
    host = repository.update(host)

    validationMessages = sorted(host.validations, key=lambda x: x.propertyName)

    assertEquals(2, len(validationMessages))

    assertEquals(ValidationMessage.Level.WARNING, validationMessages[0].level)
    assertEquals('Infrastructure/Host-Lookup-vaultlookuptest', validationMessages[0].ciId)
    assertEquals('password', validationMessages[0].propertyName)
    assertTrue(
        'WRONG_KEY' in validationMessages[0].message
        and 'password' in validationMessages[0].message
        and 'Configuration/LookupProvider-vaultlookuptest' in validationMessages[0].message,
        'Test failed: missing key validation message is not as expected')

    assertEquals(ValidationMessage.Level.WARNING, validationMessages[1].level)
    assertEquals('Infrastructure/Host-Lookup-vaultlookuptest', validationMessages[1].ciId)
    assertEquals('port', validationMessages[1].propertyName)
    assertTrue(
        'to integer field' in validationMessages[1].message
        and 'port' in validationMessages[1].message,
        'Test failed: validation message should contain:'
        ' "to integer field" and "port"')


finally:
    repository.delete(host.id)
    repository.delete(provider.id)
    repository.delete(vaultServer.id)
