env = create_random_environment_with_yak_server()

depl = deployment.prepareInitial("Applications/PlaceholderApp2/1.0", env.id)
try:
    depl2 = deployment.prepareAutoDeployeds(depl)
except:
    pass
else:
    raise "Should fail because placeholder not found"

dict = create_random_dict({'entries':{'ENV_NAME': 'yak'}})

yakEnvToUpdate = repository.read(env.id)
yakEnvToUpdate.dictionaries = [dict.id]
repository.update(yakEnvToUpdate)

depl2 = deployment.prepareAutoDeployeds(depl)
assertEquals(2, len(depl2.deployeds))

ds = [i for i in depl2.deployeds if "testFor" in i.name]
assertEquals("testForyak", ds[0].name)
