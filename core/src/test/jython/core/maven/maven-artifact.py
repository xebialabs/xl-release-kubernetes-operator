app = create_random_application("maven-artifact")
package = repository.create(factory.configurationItem("%s/1.0" % app.id, "udm.DeploymentPackage", {}))

fileUri = 'maven:com.xebialabs:artifact:1.0'
ci = factory.configurationItem('%s/mavenArtifact' % package.id, 'test-v3.DummyFileArtifact', {'fileUri': fileUri})
createdArtifact = repository.create(ci)
assertEquals('756030e5b496ad860bd41cbf25ff1ec6617ba86a3da361d8e7dd20be39f61714', createdArtifact.checksum)
