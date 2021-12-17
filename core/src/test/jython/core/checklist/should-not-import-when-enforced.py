
app = repository.create(factory.configurationItem("Applications/ChecklistApp", "udm.Application", {"verifyChecklistPermissionsOnCreate": "true"}))

switchUser(deployUsername)

try:
	deployit.importPackage("ChecklistApp/2.0")
except:
	pass
else:
	raise Exception("Should not be allowed to import application")

switchUser('admin')
assertFalse(repository.exists("Applications/ChecklistApp/2.0"))

# cleanup
repository.delete(app.id)
