security.revoke('login', 'security-model-user')

try:
    switchUser('security-model-user')
except:
	# Pass
	switchUser("admin")
else:
	raise Exception("Should not be allowed to login")

security.grant('login', 'security-model-user')

switchUser('security-model-user')

deployit.info()
