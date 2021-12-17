def login(name):
	security.logout()
	if name == 'admin':
		security.login(name, name)
	else:
		security.login(name, DEFAULT_PASSWORD)

package = deployit.importPackage('IssuesApp2/1.0')

security.createUser('issues-user-test', DEFAULT_PASSWORD)
security.assignRole('issues-user-test', ['issues-user-test'])
security.grant('login', 'issues-user-test')

login('issues-user-test')

try:
	repository.read(package.id)
except:
	login('admin')
else:
	raise Exception("should not read.")

security.createUser('issues-user-bar', DEFAULT_PASSWORD)
security.assignRole('issues-user-bar', ['issues-user-bar'])
security.grant('login', 'issues-user-bar')

login('issues-user-test')

try:
	repository.read(package.id)
except:
	login('admin')
else:
	raise Exception("should not read.")

security.login('admin', 'admin')
security.revoke('login', 'issues-user-test')
security.revoke('login', 'issues-user-bar')


security.removeRole('issues-user-test')
security.removeRole('issues-user-bar')

security.deleteUser('issues-user-test')
security.deleteUser('issues-user-bar')
repository.delete(package.application)
