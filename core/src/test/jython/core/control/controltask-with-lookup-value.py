provider = create_random_configuration('LookupProvider', 'lookup.SimpleLookupValueProvider', {'encryptedEntries':{'HOST_PASSWD': 'supersecretpassword'}})
host = create_random_host('Host-Lookup', 'overthere.SshHost', {'os':'unix', 'address':'somewhere', 'username':'somename'})

# The password is not set on the host
host = repository.read(host.id)
assertNone(host.password)

# It is configured as a "lookup-value"
host.lookup["password"] = provider, "HOST_PASSWD"
repository.update(host)

# When a control task is created, it is set.
control = deployit.prepareControlTask(host, "checkConnection")
assertNotNone(control.configurationItem.password)
assertNotEquals(control.configurationItem.password, 'supersecretpassword') # encrypted
repository.delete(host.id)
