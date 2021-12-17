try:
    constructedEnv = repository.construct('udm.Environment')
    assertEquals(None, constructedEnv._ci.getProperty('smtpServer'))
    assertEquals('udm.Environment', constructedEnv.type)

    smtp = factory.configurationItem('Configuration/defaultSmtpServer', 'mail.SmtpServer', {'host': 'localhost', 'port': '25', 'fromAddress': 'me@here.com'})
    repository.create(smtp)

    constructedEnv = repository.construct('udm.Environment')
    assertEquals('Configuration/defaultSmtpServer', constructedEnv._ci.getProperty('smtpServer'))
    assertEquals('udm.Environment', constructedEnv.type)

    constructedEnv.id = 'Environments/defaultTest-env'
    env = repository.create(constructedEnv)
    assertEquals('Configuration/defaultSmtpServer', env._ci.getProperty('smtpServer'))
    assertEquals('udm.Environment', env.type)
    assertEquals('Environments/defaultTest-env', env.id)

    repository.rename('Configuration/defaultSmtpServer', 'defaultSmtpServer1')

    env = repository.read(env.id)
    assertEquals('Configuration/defaultSmtpServer1', env._ci.getProperty('smtpServer'))

finally:
    repository.delete(env.id)
    repository.delete('Configuration/defaultSmtpServer1')
