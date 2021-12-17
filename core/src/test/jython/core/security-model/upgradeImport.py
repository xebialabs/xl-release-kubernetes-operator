repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp','udm.Application',{}))

initialPackage = deployit.importPackage("SecurityModelApp/1.0")

switchUser('security-model-user')

try:
	deployit.importPackage('SecurityModelApp/2.0')
except:
	switchUser("admin")
else:
	raise Exception("Should not be allowed to upgrade import Applications")

security.grant('import#upgrade', 'security-model-user', ['Applications/security-model-dir'])

switchUser('security-model-user')

deployit.importPackage('SecurityModelApp/2.0')

switchUser('admin')

security.revoke('import#upgrade', 'security-model-user', ['Applications/security-model-dir'])

switchUser('security-model-user')

try:
	deployit.importPackage('SecurityModelApp/3.0')
except:
	switchUser("admin")
else:
	raise Exception("Should not be allowed to upgrade import Applications")
