
id = deployit.importPackage('RepoApp2/1.0').id
id2 = deployit.importPackage('RepoApp2/2.0').id

# list all deployment packages
ids1 = repository.search('udm.DeploymentPackage', None)

assertTrue(id in ids1)
assertTrue(id2 in ids1)

idList = [id, id2]
objects = repository.read(idList)

assertEquals(2, len(objects))

# list the Applications
idsOnRoot = repository.search(None, "/Applications")
assertTrue("Applications/RepoApp2" in idsOnRoot)

# list /RepoApp2
idsOnPetClinicEar = repository.search(None, "/Applications/RepoApp2")
assertTrue("Applications/RepoApp2/1.0" in idsOnPetClinicEar)
assertTrue("Applications/RepoApp2/2.0" in idsOnPetClinicEar)

# cleanup
repository.delete('Applications/RepoApp2')
