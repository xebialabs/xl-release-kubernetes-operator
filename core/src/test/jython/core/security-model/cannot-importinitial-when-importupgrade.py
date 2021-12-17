security.grant('import#upgrade', 'security-model-user', ['Applications'])
switchUser('security-model-user')

try:
	deployit.importPackage('SecurityModelApp/1.0')
except:
	switchUser("admin")
else:
	raise Exception("Should not be allowed to initially import Applications")

security.revoke('import#upgrade', 'security-model-user')
