def createConjurServer(serverName):
    return create_random_server(
        serverName,
        'secrets.cyberark.conjur.Server',
        {
            'name': serverName,
            'serverAddress': 'http://127.0.0.1:8484',
            'account': 'xlditest',
            'username': 'admin',
            'password': 'SuperSecretPasword?123'
        },
        'Configuration'
    )

def createPolicy(serverId, policyName, path):
    return repository.create(factory.configurationItem(
        '%s/%s' % (serverId, policyName),
        'secrets.cyberark.conjur.Policy',
        {'path': path}
    ))

def createConjurDictionary(policyId, variableIds):
    return create_random_dict({
        'conjurPolicy': policyId,
        'variableIds': variableIds
    }, 'secrets.cyberark.conjur.Dictionary')
