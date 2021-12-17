

try:
    appId = createApp('proxyServer-ExportApp', 'proxyServer-folder').id
    packageId = createPackage(appId).id

    proxyServer = factory.configurationItem('Configuration/defaultProxyServer', 'credentials.ProxyServer', {'hostname': 'localhost', 'port': '8080'})
    repository.create(proxyServer)
    assertEquals('Configuration/defaultProxyServer', proxyServer.id)
    switchUser('create-ci-user')

    file2 = createFile(packageId, "proxyServer-2", "proxyServer-file2.txt", "Testni content2")
    assertNone(file2._ci.getProperty('credentials'))
    assertEquals('file.File', file2.type)
    assertNone(file2._ci.getProperty('proxySettings'))

finally:
    switchUser('admin')
    repository.delete(appId)
    repository.delete(packageId)
    repository.delete(file2.id)
    repository.delete('Configuration/defaultProxyServer')

