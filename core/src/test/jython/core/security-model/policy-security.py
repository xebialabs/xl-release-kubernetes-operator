#
ci = factory.configurationItem('Configuration/policy-taskPolicy', 'policy.TaskRetentionPolicy', {'taskRetention': '0'})

try:
    security.createUser('policy-dev-user', DEFAULT_PASSWORD)
    security.createUser('policy-adm-user', DEFAULT_PASSWORD, True)
    security.assignRole('policy-developers-role', ['policy-dev-user'])
    security.assignRole('admin', ['policy-adm-user'])
    for role in ['policy-developers-role', 'admin']:
        security.grant('login', role)
        security.grant('read', role, ['Configuration'])
        security.grant('repo#edit', role, ['Configuration'])
    security.grant('admin', 'admin')

    security.logout()
    security.login('policy-dev-user', DEFAULT_PASSWORD)
    failedCi = repository.create(ci)
    assertEquals(1, len(failedCi.validations))
    assertEquals('The operation is only allowed to admin users.', failedCi.validations[0].message)
    assertFalse(repository.exists(ci.id))

    security.logout()
    security.login('policy-adm-user', DEFAULT_PASSWORD)
    createdCi = repository.create(ci)
    assertEquals(0, len(createdCi.validations))
    assertTrue(repository.exists(ci.id))
finally:
    security.login('admin', 'admin')
    repository.delete(ci.id)
    security.deleteUser('policy-dev-user')
    security.deleteUser('policy-adm-user')
    security.removeRole('policy-developers-role')
    security.removeRole('admin')
