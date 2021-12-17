server1 = create_random_yak_server()
server2 = create_random_yak_server()
dict1 = create_random_dict({'entries':{'foo':'Alice','bar':'Bob'}, 'restrictToContainers': [server2.id]})
dict2 = create_random_dict({'entries':{'foo':'Mallory','bar':'Eve'}})

env1 = create_random_environment("with-restricted-dicts-1", [server1.id], [dict1.id, dict2.id])
env2 = create_random_environment("with-restricted-dicts-2", [server1.id])

depl = deployment.prepareInitial("Applications/PlaceholderApp/3.0", env1.id)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals('Mallory', depl.deployeds[0].placeholders['foo'])
assertEquals('Eve', depl.deployeds[0].placeholders['bar'])
