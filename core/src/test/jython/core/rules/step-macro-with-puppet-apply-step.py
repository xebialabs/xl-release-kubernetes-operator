
# Importing package

yakPackage = deployit.importPackage('PuppetModule/1.0')

# Creating infrastruture
myhost = repository.create(factory.configurationItem("Infrastructure/rules-RulesHost","overthere.LocalHost",{"os" : os_family() }))

yakServer1 = repository.create(factory.configurationItem("Infrastructure/rules-yakRuleServerPuppet1","yak.YakServer", {"host": myhost.id }))

# Creating the Environment
yakEnv = repository.create(factory.configurationItem("Environments/rules-StepMacroPuppetApplyStepEnv", "udm.Environment", {"members": [yakServer1.id]}))

# Generating Deployeds
depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)


assertNotNone(depl.deployeds)

taskid = deployment.createDeployTask(depl).id
steps  = tasks.steps(taskid).steps
task   = task2.get(taskid)

assertEquals(2, len(steps))

exceptedStep1 = "Create manifest on rules-yakRuleServerPuppet1"

assertEquals(exceptedStep1, steps[0].description)

# Cleanup the tasks
deployit.cancelTask(taskid)
repository.delete("Applications/PuppetModule")
repository.delete(yakEnv.id)
repository.delete(yakServer1.id)
repository.delete(myhost.id)