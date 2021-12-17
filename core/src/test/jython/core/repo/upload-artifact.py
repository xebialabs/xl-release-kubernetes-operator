app = repository.create(factory.configurationItem("Applications/repo-DummyApp", "udm.Application", {}))
package = repository.create(factory.configurationItem("Applications/repo-DummyApp/1.0", "udm.DeploymentPackage", {'application':'Applications/repo-DummyApp'}))

artifactAndData = factory.artifact(package.id + "/dummy.file", "test-v3.DummyArtifact", {'foo':'bar'},"**********")
artifactAndData.filename = "dummy.file"

aFromRepo = repository.create(artifactAndData)

if len(aFromRepo.validations) != 0:
    raise Exception("Validation failure: " + aFromRepo.validations)

if aFromRepo.values["foo"] == None:
    raise Exception("Create was not correct: expected \"bar\" but got None")

if aFromRepo.values["foo"] != "bar":
    raise Exception("Create was not correct: expected \"bar\" but got \"" + updatedFromRepo.values["foo"] + "\"")

updatedArtifactWithoutData = factory.configurationItem(artifactAndData.artifact.id, str(artifactAndData.artifact.type), {'foo':'baz'})
updatedFromRepo = repository.update(updatedArtifactWithoutData)

if updatedFromRepo.values["foo"] == None:
    raise Exception("Update was not correct: expected \"baz\" but got None")

if updatedFromRepo.values["foo"] != "baz":
    raise Exception("Update was not correct: expected \"baz\" but got \"" + updatedFromRepo.values["foo"] + "\"")

repository.delete(app.id)
