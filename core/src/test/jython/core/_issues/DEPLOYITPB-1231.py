from java.util import ArrayList

folderCiId = 'Applications/issues-DEPL-1231'

appCis = ArrayList()
appCiId1 = folderCiId + '/issues-someApp1'
appCis.add(appCiId1)
appCiId2 = folderCiId + '/issues-someApp2'
appCis.add(appCiId2)

repository.create(factory.configurationItem(folderCiId,'core.Directory',{}))
repository.create(factory.configurationItem(appCiId1, 'udm.Application', {}))
repository.create(factory.configurationItem(appCiId2, 'udm.Application', {}))

assertTrue(repository.exists(appCiId1))
assertTrue(repository.exists(appCiId2))

repository.deleteList(appCis)

assertFalse(repository.exists(appCiId1))
assertFalse(repository.exists(appCiId2))

repository.delete(folderCiId)
