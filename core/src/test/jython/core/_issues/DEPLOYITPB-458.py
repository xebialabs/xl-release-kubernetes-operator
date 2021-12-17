dummyHost = repository.create(factory.configurationItem('Infrastructure/issues-dummyHost', "test-v3.DummyHost", {'accessMethod':'SSH_SFTP','os':'UNIX','address':'myServer', 'username':'foo', 'password':'bar'}))

dummyServer = repository.create(factory.configurationItem("Infrastructure/issues-dummyJeeServer", "test-v3.DummyJeeServer", {'hostName':dummyHost.id}))

dictObj = {'str_prop_placeholder':'strValue','int_prop_placeholder':'10', 'bool_prop_placeholder':'true', 'enum_prop_placeholder':'DUMMY3'}
dummyDict = repository.create(factory.configurationItem('Environments/issues-dummyDict', 'udm.Dictionary',{'entries':dictObj}))
dummyEnv = repository.create(factory.configurationItem("Environments/issues-dummyEnv", "udm.Environment", {"members": [dummyServer.id], "dictionaries": [dummyDict.id]}))

assertEquals('strValue',dummyDict.entries['str_prop_placeholder'])
assertEquals('10',dummyDict.entries['int_prop_placeholder'])
assertEquals('true',dummyDict.entries['bool_prop_placeholder'])

dictPackage = deployit.importPackage('IssuesApp5/1.0-for-dict')
dictPackage2 = deployit.importPackage('IssuesApp5/2.0-for-dict')
dummyEar1 = repository.read(dictPackage.id + '/dummyEar')
dummyEar2 = repository.read(dictPackage2.id + '/dummyEar')

dummyEar1.stringProp='{{str_prop_placeholder}}'
dummyEar1.integerProp='{{int_prop_placeholder}}'
dummyEar1.booleanProp='{{bool_prop_placeholder}}'
dummyEar1.enumProp='{{enum_prop_placeholder}}'

dummyEar2.stringProp='{{str_prop_placeholder}}'

updatedEar = repository.update(dummyEar1)
updatedEar = repository.update(dummyEar2)

#first dictionary in an env with a specific key wins.
anotherDict = repository.create(factory.configurationItem('Environments/issues-anotherDict', 'udm.Dictionary',{'entries':{'str_prop_placeholder':'anotherStrValue'}}))
dummyEnv.dictionaries=[dummyDict.id, anotherDict.id]
assertEquals('anotherStrValue',anotherDict.entries['str_prop_placeholder'])

repository.update(dummyEnv)

depl = deployment.prepareInitial(dictPackage.id, dummyEnv.id)
deployeds = deployment.generateSingleDeployed(dictPackage.id + '/dummyEar', dummyServer.id, depl).deployeds
assertEquals(1, len(deployeds))

deployed = deployeds[0]
deployed.prettyprint()
assertEquals('strValue', deployed.stringProp)
assertEquals(10, deployed.integerProp)
assertEquals(True, deployed.booleanProp)
assertEquals('DUMMY3', deployed.enumProp)

deployed.stringProp = 'updatedStrValue'
depl.deployeds = [deployed]
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

#Even if values from a dictionary were overridden by the user in a previous deployment,
# an upgrade will still take the then-current values from the dictionary
deploymentId = dummyEnv.id + '/IssuesApp5'
upgradedDeployed = deployment.prepareUpgrade(dictPackage2.id, deploymentId).deployeds[0]
upgradedDeployed.prettyprint()
assertEquals('strValue', upgradedDeployed.stringProp)

# Use "auto property" dictionary keys:

# Set property to blank in deployable so it will be replaced.
dummyEar1 = repository.read(dictPackage.id + '/dummyEar')
dummyEar1.stringProp=''
updatedEar = repository.update(dummyEar1)

autoPropertyDictObj = {'test-v3.DeployedDummyEarWithAllProperties.stringProp': 'autoProperty'}
autoPropertyDict = repository.create(factory.configurationItem('Environments/issues-autoPropertyDict', 'udm.Dictionary',{'entries':autoPropertyDictObj}))
# added dummyDict in order to avoid missingPlaceholders exception being thrown for the rest of string properties in deployable
autoPropertyEnv = repository.create(factory.configurationItem("Environments/issues-autoPropertyEnv", "udm.Environment",
                                                              {"members": [dummyServer.id],
                                                               "dictionaries": [autoPropertyDict.id, dummyDict.id]}))

depl = deployment.prepareInitial(dictPackage.id, autoPropertyEnv.id)
deployeds = deployment.generateSingleDeployed(dictPackage.id + '/dummyEar', dummyServer.id, depl).deployeds
assertEquals(1, len(deployeds))

deployed = deployeds[0]
deployed.prettyprint()
assertEquals('autoProperty', deployed.stringProp)

repository.delete(autoPropertyEnv.id)
repository.delete(autoPropertyDict.id)
repository.delete(dummyEnv.id)
repository.delete(dummyDict.id)
repository.delete(dummyServer.id)
repository.delete(dummyHost.id)
repository.delete(anotherDict.id)
