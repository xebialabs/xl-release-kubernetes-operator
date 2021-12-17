app = create_random_application("embedded_artifact_EmbeddedArtifactApp")
embeddedArtifactAppPackage_1_0 = repository.create(factory.configurationItem("%s/1.0" % app.id, 'udm.DeploymentPackage', {}))
embeddedArtifactDeployable = repository.create(factory.configurationItem("%s/embeddedDeployable" % embeddedArtifactAppPackage_1_0.id, 'test.ParentDeployable', {}))

placeholder_file = open('src/test/resources/testfiles/placeholders.txt', "r").read()
artifactAndData = factory.artifact('%s/attachedArtifact' % embeddedArtifactDeployable.id, 'test.ChildEmbeddedDeployable', {}, placeholder_file)
artifactAndData.filename = 'placeholders.txt'
embeddedArtifact = repository.create(artifactAndData)

assertEquals('internal:placeholders.txt', embeddedArtifact.fileUri)

expectedPlaceholders = ["foo", "bar"]

assertEquals(2, len(embeddedArtifact.placeholders))
