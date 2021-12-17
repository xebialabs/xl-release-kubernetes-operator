conjurServer = createConjurServer('Conjur')
host = create_random_server(
    'Conjur-Host-Lookup',
    'overthere.SshHost',
    {'os':'unix', 'address':'somewhere', 'username':'somename'}
)

policy = createPolicy(conjurServer.id, 'RootPolicy', 'itest')
provider = create_random_configuration(
    'LookupProvider',
    'secrets.cyberark.conjur.LookupValueProvider',
    {'conjurPolicy' : policy.id}
)

# The password is not set on the host
host = repository.read(host.id)
assertNone(host.password)

# It is configured as a "lookup-value"
previousLookup = host.lookup["password"]
host.lookup["password"] = provider, "ssh_host_passwd"
repository.update(host)

# When a control task is created, it is set.
control = deployit.prepareControlTask(host, "checkConnection")
assertNotNone(control.configurationItem.password)
assertNotEquals(control.configurationItem.password, 'supersecretpassword') # encrypted
repository.delete(host.id)
