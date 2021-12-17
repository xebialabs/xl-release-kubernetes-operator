# Importing package

yakPackage = deployit.importPackage('StagingApp/1.0')

# Creating infrastruture

yakServer1 = repository.create(factory.configurationItem("Infrastructure/staging-yakHostServer","yak.YakStagingServer", { 'stagingDir': '/tmp/stage1'}))

# Creating the Environment
yakEnv = repository.create(factory.configurationItem("Environments/staging-StagingEnv", "udm.Environment", {"members": [yakServer1.id]}))

# Generating Deployeds
depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)

taskid = deployment.createDeployTask(depl).id
steps = tasks.steps(taskid).steps

stepsdescription1 = steps[0].description
stepsdescription2 = steps[1].description
stepsdescription4 = steps[4].description

exceptedStep1 = "Upload test.yak to staging-yakHostServer"
exceptedStep2 = "Upload yak2.yak to staging-yakHostServer"
# Verifying the number of steps generated in the Plan
assertEquals(6, len(steps))

# Verifying the Staging step is getting generated 
assertEquals(exceptedStep1, stepsdescription1)
assertEquals(exceptedStep2, stepsdescription2)

# Cleanup the tasks 
deployit.cancelTask(taskid)
repository.delete("Applications/StagingApp")
repository.delete(yakEnv.id)
repository.delete(yakServer1.id)
