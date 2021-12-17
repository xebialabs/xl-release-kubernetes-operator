from com.xebialabs.deployit.plugin.api.validation import ValidationMessage

provider = create_random_configuration(
    'LookupProvider-lookuptest',
    'lookup.SimpleLookupValueProvider',
    {
        'entries':{'HOST_PORT': '22', 'HOSTNAME': 'localhost'},
        'encryptedEntries':{'HOST_PASSWD': 'supersecretpassword'}
    }
)
host = create_random_host(
    'Host-Lookup-lookuptest',
    'overthere.SshHost',
    {'os':'unix', 'address':'somewhere', 'username':'somename'}
)

# The password is not set on the host
host = repository.read(host.id)
assertNone(host.password)

# with wrong key and wrong type
host.lookup["password"] = provider, "WRONG_KEY"
host.lookup["port"] = provider, "HOSTNAME"
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
    ' "cannot be accessed to resolve value for field", "port" and "%s"' % provider.id)

# with correct key and correct type
host.lookup["password"] = provider, "HOST_PASSWD"
host.lookup["port"] = provider, "HOST_PORT"
host = repository.update(host)

validationMessages = host.validations

assertEquals(0, len(validationMessages))

repository.delete(host.id)
