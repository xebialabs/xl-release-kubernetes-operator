from com.xebialabs.deployit.plugin.api.validation import ValidationMessage

conjurServer = createConjurServer('ConjurServer-Validation')
policy = createPolicy(conjurServer.id, 'RootPolicy', 'itest')
provider = create_random_configuration(
    'LookupProvider-conjurlookuptest',
    'secrets.cyberark.conjur.LookupValueProvider',
    {'conjurPolicy' : policy.id}
)
host = create_random_server(
    'Host-Lookup-conjurlookuptest',
    'overthere.SshHost',
    {'os':'unix', 'address':'somewhere', 'username':'somename'}
)

# The password is not set on the host
host = repository.read(host.id)
assertNone(host.password)

# with wrong key and wrong type
host.lookup["password"] = provider, "WRONG_KEY"
host.lookup["port"] = provider, "ssh_host_passwd"
host = repository.update(host)

validationMessages = sorted(host.validations, key=lambda x: x.propertyName)

assertEquals(2, len(validationMessages))

assertEquals(ValidationMessage.Level.WARNING, validationMessages[0].level)
assertEquals(host.id, validationMessages[0].ciId)
assertEquals('password', validationMessages[0].propertyName)
assertTrue(
    'WRONG_KEY' in validationMessages[0].message
    and 'password' in validationMessages[0].message
    and provider.id in validationMessages[0].message,
    'Test failed: missing key validation message is not as expected')

assertEquals(ValidationMessage.Level.WARNING, validationMessages[1].level)
assertEquals(host.id, validationMessages[1].ciId)
assertEquals('port', validationMessages[1].propertyName)
assertTrue(
    'to integer field' in validationMessages[1].message
    and 'port' in validationMessages[1].message,
    'Test failed: validation message should contain:'
    ' "to integer field" and "port"')
repository.delete(host.id)
