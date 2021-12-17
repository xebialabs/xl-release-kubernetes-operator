repository.create(factory.configurationItem('Applications/repo-accessMgmtDAR', 'udm.Application', {}))
repository.create(factory.configurationItem('Applications/repo-accessMgmtDAR/1.5.0', 'udm.DeploymentPackage', {}))

archive = open('src/test/resources/testfiles/archive.zip', "rb").read()
artifactAndData = factory.artifact('Applications/repo-accessMgmtDAR/1.5.0/zipArtifact', 'test-v3.DummyFolderArtifact', {}, archive)
artifactAndData.filename = 'zipArtifact.zip'
repository.create(artifactAndData)

try:
    artifactAndData = factory.artifact('Applications/repo-accessMgmtDAR/1.5.0/nonZipArtifact', 'test-v3.DummyFolderArtifact', {}, [])
    artifactAndData.filename = 'nonZipArtifact'
    repository.create(artifactAndData)
except:
    pass
else:
    raise "It should not be allowed to create a ZIP folder without proper archive file"


repository.delete('Applications/repo-accessMgmtDAR')