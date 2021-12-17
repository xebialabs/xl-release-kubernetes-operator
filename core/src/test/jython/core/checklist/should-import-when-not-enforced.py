
# This behavior is needed for backwards compatibility, and is the default behavior.

app = repository.create(factory.configurationItem("Applications/ChecklistApp", "udm.Application", {"verifyChecklistPermissionsOnCreate": "false"}))

switchUser(deployUsername)
importedPackage = deployit.importPackage("ChecklistApp/2.0")

switchUser('admin')
appImported = repository.read("Applications/ChecklistApp/2.0")
assertEquals(appImported.satisfiesReleaseNotes, True)

# cleanup
repository.delete(app.id)
