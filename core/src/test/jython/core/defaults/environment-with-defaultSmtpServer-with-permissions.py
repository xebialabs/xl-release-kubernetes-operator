try:
    constructedEnv = repository.construct('udm.Environment')
    assertEquals(None, constructedEnv._ci.getProperty('smtpServer'))
    assertEquals('udm.Environment', constructedEnv.type)
    smtp = factory.configurationItem('Configuration/defaultSmtpServer', 'mail.SmtpServer', {'host': 'localhost', 'port': '25', 'fromAddress': 'me@here.com'})
    repository.create(smtp)

    switchUser('create-ci-user')

    constructedEnv = repository.construct('udm.Environment')
    assertEquals('udm.Environment', constructedEnv.type)
    assertNone(constructedEnv._ci.getProperty('smtpServer'))

    constructedEnv.id = 'Environments/defaultTest-env'
    env = repository.create(constructedEnv)
    assertEquals('udm.Environment', env.type)
    assertEquals('Environments/defaultTest-env', env.id)
    assertNone(env._ci.getProperty('smtpServer'))
finally:
    switchUser('admin')
    repository.delete(env.id)
    repository.delete('Configuration/defaultSmtpServer')