from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File

# Setup
tempDir = TemporaryDirectoryHolder.getTemporaryDirectory()
dirCi = repository.create(factory.configurationItem('Infrastructure/control-task-dir-dsfs','core.Directory',{}))

ci = repository.create(factory.configurationItem(dirCi.id + '/ctServer', 'yak.StartableContainer',{'tempDir':tempDir.path, 'startFileName':'ctServer.started'}))

startFile = File(tempDir, 'ctServer.started')
assertFalse(startFile.exists())

security.createUser('controltask', DEFAULT_PASSWORD)
security.assignRole('controltask', ['controltask'])
security.grant('login', 'controltask')
security.grant('read','controltask',[dirCi.id])
security.logout()
security.login('controltask', DEFAULT_PASSWORD)

# Execute control task
try:
	deployit.executeControlTask("start", ci)
except:
	security.logout()
	security.login('admin','admin')
	security.grant('controltask#execute','controltask', [dirCi.id])
	security.logout()
	security.login('controltask', DEFAULT_PASSWORD)
else:
	raise Exception("Should be covered by security restrictions")

try:
	deployit.executeControlTask("start", ci)
	assertTrue(startFile.exists())
finally:
	security.logout()
	security.login('admin','admin')
	security.revoke('login', 'controltask')
	security.revoke('read','controltask',[dirCi.id])
	security.revoke('controltask#execute', 'controltask')
	security.deleteUser("controltask")
	security.removeRole('controltask')
	
	repository.delete(dirCi.id)
	startFile.delete()
