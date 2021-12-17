def login(name):
	security.logout()
	if name == 'admin':
		security.login(name, name)
	else:
		security.login(name, DEFAULT_PASSWORD)

package = deployit.importPackage('SecurityModelApp/1.0')

security.createUser('security-model-foo-user', DEFAULT_PASSWORD)
security.assignRole('security-model-foo-user', ['security-model-foo-user'])
security.grant('login', 'security-model-foo-user')

login('security-model-foo-user')

try:
	repository.read(package.id)
except:
	login('admin')
else:
	raise Exception("should not read.")

security.createUser('security-model-bar-user', DEFAULT_PASSWORD)
security.assignRole('security-model-bar-user', ['security-model-bar-user'])
security.grant('login', 'security-model-bar-user')

login('security-model-foo-user')

try:
	repository.read(package.id)
except:
	login('admin')
else:
	raise Exception("should not read.")

security.deleteUser('security-model-foo-user')
security.removeRole('security-model-foo-user')
security.deleteUser('security-model-bar-user')
security.removeRole('security-model-bar-user')
repository.delete(package.application)
