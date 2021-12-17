# Should not be able to save artifacts with bad 'fileUri'

myApp = create_random_application("artifacts-RemoteArtifactApp")
package1 = repository.create(factory.configurationItem("%s/1.0" % myApp.id, "udm.DeploymentPackage", {}))

artifactAndData = factory.configurationItem('%s/zipArtifact' % package1.id, 'test-v3.DummyFolderArtifact', {'fileUri': 'wrong:foo/bar'})

try:
    createdArtifact = repository.create(artifactAndData)
except:
    pass
else:
    fail("We expect an exception here")
