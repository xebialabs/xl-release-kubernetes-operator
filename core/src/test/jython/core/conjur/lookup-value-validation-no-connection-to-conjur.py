from com.xebialabs.deployit.plugin.api.validation import ValidationMessage

conjurServer = createConjurServer('ConjurServer-noConnection')
conjurServer.serverAddress = 'http://127.0.0.1:28201'
repository.update(conjurServer)
policy = createPolicy(conjurServer.id, 'RootPolicy', 'itest')
provider = create_random_configuration(
    'LookupProvider-conjurlookuptestnocon',
    'secrets.cyberark.conjur.LookupValueProvider',
    {'conjurPolicy' : policy.id}
)
host = create_random_server(
    'Host-Lookup-conjurlookuptestnocon',
    'overthere.SshHost',
    {'os':'unix', 'address':'somewhere', 'username':'somename'}
)

# The password is not set on the host
host = repository.read(host.id)
assertNone(host.password)

# with wrong key and wrong type
host.lookup["password"] = provider, "ssh_host_passwd"
host.lookup["port"] = provider, "ssh_host_passwd"
host = repository.update(host)

validationMessages = sorted(host.validations, key=lambda x: x.propertyName)
print "Printing validation messages!!!!"
print validationMessages
assertEquals(2, len(validationMessages))

assertEquals(ValidationMessage.Level.WARNING, validationMessages[0].level)
assertEquals(host.id, validationMessages[0].ciId)
assertEquals('password', validationMessages[0].propertyName)
assertTrue(
    'cannot be accessed to resolve value for field' in validationMessages[0].message
    and 'password' in validationMessages[0].message
    and provider.id in validationMessages[0].message,
    "Test failed: validation message should contain:" +
    " 'cannot be accessed to resolve value for field', 'password' and '%s' but message was '" % provider.id
    +  validationMessages[0].message + "'")

assertEquals(ValidationMessage.Level.WARNING, validationMessages[1].level)
assertEquals(host.id, validationMessages[1].ciId)
assertEquals('port', validationMessages[1].propertyName)
assertTrue(
    'cannot be accessed to resolve value for field' in validationMessages[1].message
    and 'port' in validationMessages[1].message
    and '%s' % provider.id in validationMessages[1].message,
    "Test failed: validation message should contain:" +
    " 'cannot be accessed to resolve value for field', 'port' and '%s' but message was '" % provider.id
    +  validationMessages[1].message + "'")
repository.delete(host.id)
