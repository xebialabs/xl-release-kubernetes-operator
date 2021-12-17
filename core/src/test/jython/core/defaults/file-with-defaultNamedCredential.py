appId = createApp('credentials-ExportApp', 'credentials-folder').id
packageId = createPackage(appId).id
file1 = createFile(packageId, "credentials-1", "credentials-file1.txt", "Testni content1")

assertEquals(None, file1._ci.getProperty('credentials'))
assertEquals('file.File', file1.type)

credentials = factory.configurationItem('Configuration/defaultNamedCredential', 'credentials.UsernamePasswordCredentials', {'username': 'test', 'password': '8080'})
repository.create(credentials)
assertEquals('Configuration/defaultNamedCredential', credentials.id)

file2 = createFile(packageId, "credentials-2", "credentials-file2.txt", "Testni content2")
assertEquals('Configuration/defaultNamedCredential', file2._ci.getProperty('credentials'))
assertEquals('file.File', file2.type)

repository.rename('Configuration/defaultNamedCredential', 'defaultNamedCredential1')
file2 = repository.read(file2.id)
assertEquals('Configuration/defaultNamedCredential1', file2._ci.getProperty('credentials'))

repository.delete(appId)
repository.delete(packageId)
repository.delete(file1.id)
repository.delete(file2.id)
repository.delete('Configuration/defaultNamedCredential1')