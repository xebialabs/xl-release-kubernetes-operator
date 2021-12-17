suitePrefix = 'artifact-with-placeholders-'

# Import package
importedPackage = repository.read("Applications/EmbeddedArtifactsWithPlaceholders/2.0")

embArtFile1 = repository.read('%s/nested/{{art-file1}}-1' % importedPackage.id)
embArtFile2 = repository.read('%s/nested/{{art-file2}}-2' % importedPackage.id)

parent = repository.read('%s/nested' % importedPackage.id)

# Request defined placeholders for artifact
placeholders = sorted(placeholder.definedPlaceholders("art-file1"), key=lambda x: x.ciId)
# Assert
assertEquals(2, len(placeholders))

assertEquals('art-file1', placeholders[1].key)
assertEquals('yak.EmbeddedFileArtifact', placeholders[1].ciType)
assertEquals(embArtFile1.id, placeholders[1].ciId, )

assertEquals('art-file1', placeholders[0].key)
assertEquals('art-file1', placeholders[1].key)
# assertEquals(placeholders[3].key, 'art-file2')
# assertEquals(placeholders[4].key, 'art-file2')

# assertEquals(placeholders[5].key, 'art-first.placeholder')
# assertEquals(placeholders[5].ciType, 'EmbeddedFileArtifact')
# assertEquals(placeholders[5].ciId, 'Applications/EmbeddedArtifactsWithPlaceholders/2.0/nested/{{art-file1}}-1')

# assertEquals(placeholders[6].key, 'art-look.at.me')
# assertEquals(placeholders[6].ciType, 'EmbeddedFileArtifact')
# assertEquals(placeholders[6].ciId, 'Applications/EmbeddedArtifactsWithPlaceholders/2.0/nested/{{art-file2}}-2')
