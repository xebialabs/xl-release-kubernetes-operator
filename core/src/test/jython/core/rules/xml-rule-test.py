#DEPL -4794 Implement XML rules with deployed scope in the rule-based planner

# Importing package

yakPackage = deployit.importPackage('RulesApp/11.0')

# Creating infrastruture

yakServer1 = repository.create(factory.configurationItem("Infrastructure/rules-yakRuleServerXml1","yak.YakServer"))

yakServer2 = repository.create(factory.configurationItem("Infrastructure/rules-yakRuleServerXml2","yak.YakServer"))

# Creating the Environment
yakEnv = repository.create(factory.configurationItem("Environments/rules-XmlPlanEnv", "udm.Environment", {"members": [yakServer1.id,yakServer2.id ]}))

# Generating Deployeds
depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)


block =deployment.taskPreviewBlock(depl).blocks[0].block
block0 = block.blocks[0]
blcok1 = block.blocks[1]
previewSteps = blcok1.steps
assertEquals(9, len(previewSteps) + len(block0.steps))


taskid = deployment.createDeployTask(depl).id

steps = tasks.steps(taskid).steps
assertEquals(10, len(steps))


stepsdescription0 = steps[0].description
stepsdescription1 = steps[1].description
stepsdescription8 = steps[8].description

exceptedStep0 = "Preprocessor Notification for Rule implementation"
exceptedStep1 = "My deployed XML rule test step"
exceptedStep8 = "Log plan Yak Xml for rules"


assertEquals(exceptedStep0, stepsdescription0)
assertEquals(exceptedStep1, stepsdescription1)
assertEquals(exceptedStep8, stepsdescription8)

task2.cancel(taskid)
repository.delete("Applications/RulesApp")
repository.delete(yakEnv.id)
repository.delete(yakServer1.id)
repository.delete(yakServer2.id)