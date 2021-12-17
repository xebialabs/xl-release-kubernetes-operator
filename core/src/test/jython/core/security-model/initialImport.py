switchUser('security-model-user')

try:
	deployit.importPackage('SecurityModelApp/1.0')
except:
	switchUser("admin")
else:
	raise Exception("Should not be allowed to initially import Applications")

security.grant("import#initial", "security-model-user", ['Applications'])

switchUser('security-model-user')

importedPackage = deployit.importPackage('SecurityModelApp/1.0')

switchUser('admin')

security.revoke('import#initial', 'security-model-user', ['Applications'])

repository.delete(importedPackage.application)
