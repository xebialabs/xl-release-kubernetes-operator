# Created artifacts with uploaded files should get a 'fileUri' property

myApp = create_random_application("artifacts-RemoteArtifactApp")
package1 = repository.create(factory.configurationItem("%s/1.0" % myApp.id, "udm.DeploymentPackage", {}))

archive = open('src/test/resources/testfiles/archive.zip', "rb").read()
artifactAndData = factory.artifact('%s/attachedArtifact' % package1.id, 'test-v3.DummyFolderArtifact', {}, archive)
artifactAndData.filename = 'zipArtifact.zip'
createdArtifact = repository.create(artifactAndData)

assertEquals('internal:zipArtifact.zip', createdArtifact.fileUri)
