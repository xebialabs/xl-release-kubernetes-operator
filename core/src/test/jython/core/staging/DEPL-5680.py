# Importing package

yakPackage = deployit.importPackage('StagingApp/1.0-placeholders')

# Creating infrastruture

yakServer1 = repository.create(factory.configurationItem("Infrastructure/staging-yakHostServer","yak.YakStagingServer", { 'stagingDir': '/tmp/stage1'}))

# Creating the Environment
yakEnv = repository.create(factory.configurationItem("Environments/staging-StagingEnv", "udm.Environment", {"members": [yakServer1.id]}))

yak = factory.configurationItem(yakServer1.id + '/test.yak', 'yak.DeployedStageableYak', {'deployable':'Applications/StagingApp/1.0-placeholders/test.yak','container':yakServer1.id, 'placeholders':{'PLACEHOLDER':'same'}})
yakSamePlaceholder = factory.configurationItem(yakServer1.id + '/test2.yak', 'yak.DeployedStageableYak', {'deployable':'Applications/StagingApp/1.0-placeholders/test.yak','container':yakServer1.id, 'placeholders':{'PLACEHOLDER':'same'}})
yakDifferencePlaceholder = factory.configurationItem(yakServer1.id + '/test3.yak', 'yak.DeployedStageableYak', {'deployable':'Applications/StagingApp/1.0-placeholders/test.yak','container':yakServer1.id, 'placeholders':{'PLACEHOLDER':'different'}})

# Generating Deployeds
depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl.deployeds = [yak, yakSamePlaceholder, yakDifferencePlaceholder]

taskid = deployment.createDeployTask(depl).id
steps = tasks.steps(taskid).steps

assertEquals(7, len(steps))

# Two staging steps, three action steps
assertEquals("Upload yak-test.txt to staging-yakHostServer", steps[0].description)
assertEquals("Upload yak-test.txt to staging-yakHostServer", steps[1].description)
assertEquals("Milk the yak", steps[2].description)
assertEquals("Milk the yak", steps[3].description)
assertEquals("Milk the yak", steps[4].description)

deployit.cancelTask(taskid)
repository.delete("Applications/StagingApp")
repository.delete(yakEnv.id)
repository.delete(yakServer1.id)
