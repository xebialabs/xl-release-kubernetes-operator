
# Importing package

yakPackage = deployit.importPackage('RulesApp/10.0')

# Creating infrastruture
myhost = repository.create(factory.configurationItem("Infrastructure/rules-RuleHost-noop","overthere.LocalHost",{"os" : os_family() }))

yakServer1 = repository.create(factory.configurationItem("Infrastructure/rules-yakRuleServerMacroNoop1","yak.YakServer", {"host": myhost.id }))

# Creating the Environment
yakEnv = repository.create(factory.configurationItem("Environments/rules-StepMacroNoopEnv", "udm.Environment", {"members": [yakServer1.id]}))

# Generating Deployeds
depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)


assertNotNone(depl.deployeds)

taskid = deployment.createDeployTask(depl).id
steps  = tasks.steps(taskid).steps
task   = task2.get(taskid)

assertEquals(4, len(steps))

exceptedStep1 = "Waiting for 1 second"
exceptedStep2 = "first noop step"
exceptedStep3 = "first noop step"

assertEquals(exceptedStep1, steps[0].description)
assertEquals(exceptedStep2, steps[1].description)
assertEquals(exceptedStep3, steps[2].description)


# Cleanup the tasks
deployit.cancelTask(taskid)
repository.delete("Applications/RulesApp")
repository.delete(yakEnv.id)
repository.delete(yakServer1.id)
repository.delete(myhost.id)