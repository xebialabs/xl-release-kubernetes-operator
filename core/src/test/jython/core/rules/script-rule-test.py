
# Importing package

yakPackage = deployit.importPackage('RulesApp/10.0')

# Creating infrastruture
myhost = repository.create(factory.configurationItem("Infrastructure/rules-RuleHost","overthere.LocalHost",{"os" : os_family() }))

yakServer1 = repository.create(factory.configurationItem("Infrastructure/rules-yakRuleServerScriptRule1","yak.YakServer", {"host": myhost.id }))

# Creating the Environment
yakEnv = repository.create(factory.configurationItem("Environments/rules-ScriptPlanEnv", "udm.Environment", {"members": [yakServer1.id]}))

# Generating Deployeds
depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)


assertNotNone(depl.deployeds)

taskid = deployment.createDeployTask(depl).id
steps  = tasks.steps(taskid).steps
task   = task2.get(taskid)

stepsdescription0 = steps[0].description
stepsdescription1 = steps[1].description
stepsdescription2 = steps[2].description
stepsdescription3 = steps[3].description
stepsdescription4 = steps[4].description
stepsdescription5 = steps[5].description



assertEquals(7, len(steps))

exceptedStep0 = "Preprocessor Notification for Rule implementation"
exceptedStep1 = "Waiting for 1 second"
exceptedStep2 = "My deployed rule test step"
exceptedStep3 = "My deployed rule test step"
exceptedStep4 = "Log plan Yak Xml for rules"
exceptedStep5 = "Postprocessor Notification for Rule implementation"


assertEquals(exceptedStep0, stepsdescription0)
assertEquals(exceptedStep1, stepsdescription1)
assertEquals(exceptedStep2, stepsdescription2)
assertEquals(exceptedStep3, stepsdescription3)
assertEquals(exceptedStep4, stepsdescription4)
assertEquals(exceptedStep5, stepsdescription5)


# Cleanup the tasks
deployit.cancelTask(taskid)
repository.delete("Applications/RulesApp")
repository.delete(yakEnv.id)
repository.delete(yakServer1.id)
repository.delete(myhost.id)