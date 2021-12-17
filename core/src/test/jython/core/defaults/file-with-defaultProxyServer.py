appId = createApp('proxyServer-ExportApp', 'proxyServer-folder').id
packageId = createPackage(appId).id
file1 = createFile(packageId, "proxyServer-1", "proxyServer-file1.txt", "Testni content1")

assertEquals(None, file1._ci.getProperty('proxySettings'))
assertEquals(None, file1._ci.getProperty('credentials'))
assertEquals('file.File', file1.type)

proxyServer = factory.configurationItem('Configuration/defaultProxyServer', 'credentials.ProxyServer', {'hostname': 'localhost', 'port': '8080'})
repository.create(proxyServer)


assertEquals('Configuration/defaultProxyServer', proxyServer.id)

file2 = createFile(packageId, "proxyServer-2", "proxyServer-file2.txt", "Testni content2")
assertEquals('Configuration/defaultProxyServer', file2._ci.getProperty('proxySettings'))
assertEquals(None, file2._ci.getProperty('credentials'))
assertEquals('file.File', file2.type)

repository.rename('Configuration/defaultProxyServer', 'defaultProxyServer1')
file2 = repository.read(file2.id)
assertEquals('Configuration/defaultProxyServer1', file2._ci.getProperty('proxySettings'))


repository.delete(appId)
repository.delete(packageId)
repository.delete(file1.id)
repository.delete(file2.id)
repository.delete('Configuration/defaultProxyServer1')