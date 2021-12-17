app = create_random_application("maven-missing-artifact")
package = repository.create(factory.configurationItem("%s/1.0" % app.id, "udm.DeploymentPackage", {}))

fileUri = 'maven:com.xebialabs:no-artifact:1.0'
ci = factory.configurationItem('%s/no-mavenArtifact' % package.id, 'test-v3.DummyFileArtifact', {'fileUri': fileUri})
try:
    createdArtifact = repository.create(ci)
except:
    pass
else:
    fail("Excepted error as artifact does not exist")
