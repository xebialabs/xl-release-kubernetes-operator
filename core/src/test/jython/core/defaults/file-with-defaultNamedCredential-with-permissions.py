try:
    appId = createApp('credentials-ExportApp', 'credentials-folder').id
    packageId = createPackage(appId).id

    credentials = factory.configurationItem('Configuration/defaultNamedCredential', 'credentials.UsernamePasswordCredentials', {'username': 'test', 'password': '8080'})
    repository.create(credentials)
    assertEquals('Configuration/defaultNamedCredential', credentials.id)

    switchUser('create-ci-user')

    file2 = createFile(packageId, "credentials-2", "credentials-file2.txt", "Testni content2")
    assertEquals('file.File', file2.type)
    assertNone(file2._ci.getProperty('credentials'))
finally:
    switchUser('admin')
    repository.delete(appId)
    repository.delete(packageId)
    repository.delete(file2.id)

    repository.delete('Configuration/defaultNamedCredential')

