dict = create_random_dict({'entries':{'computer':'The Machine'}})
encryptedDict = create_random_dict({'entries':{'asset':'John Reese'}}, 'udm.EncryptedDictionary')
server = create_random_yak_server()
env = create_random_environment('effective-dictionary', [server.id], [dict.id, encryptedDict.id])

dictMap = deployment.effectiveDictionary(env.id, None, None)
assertEquals("The Machine", dictMap["computer"])
assertNotEquals("John Reese", dictMap["asset"])
