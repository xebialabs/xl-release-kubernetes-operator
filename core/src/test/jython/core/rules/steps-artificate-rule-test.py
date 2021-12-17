
# Importing package

yakPackage = deployit.importPackage('RulesApp/12.0')

# Creating infrastructure

myhost = repository.create(factory.configurationItem("Infrastructure/rules-RulesHost","overthere.LocalHost",{"os" : os_family() }))

yakServer1 = repository.create(factory.configurationItem("Infrastructure/rules-yakRuleServerHo1","yak.YakServer", {"host": myhost.id}))

# Creating the Environment
yakEnv = repository.create(factory.configurationItem("Environments/rules-StepPlanEnv", "udm.Environment", {"members": [yakServer1.id]}))

# Generating Deployeds
depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)


assertNotNone(depl.deployeds)

taskid = deployment.createDeployTask(depl).id
taskWithSteps = tasks.steps(taskid)

assertEquals("itest.myWaitStep", taskWithSteps.getStep(1).metadata["rule"])
assertEquals("50", taskWithSteps.getStep(1).metadata["order"])
assertEquals("false", taskWithSteps.getStep(1).metadata["previewAvailable"])


assertEquals("itest.myLocalPython", taskWithSteps.getStep(4).metadata["rule"])
assertEquals("70", taskWithSteps.getStep(4).metadata["order"])
assertEquals("true", taskWithSteps.getStep(4).metadata["previewAvailable"])

steps = tasks.steps(taskid).steps
task  = task2.get(taskid)

stepsdescription1 = steps[0].description
stepsdescription2 = steps[1].description
stepsdescription3 = steps[2].description
stepsdescription4 = steps[3].description
stepsdescription5 = steps[4].description



assertEquals(6,len(steps))

exceptedStep1 = "Waiting for 1 second"
exceptedStep2 = "Deploy resolve template test1.yak to rules-yakRuleServerHo1"
exceptedStep3 = "Create test1.yak on rules-yakRuleServerHo1"
exceptedStep4 = "Run the 'welcome_user1.py' script"
exceptedStep5 = "Run the 'welcome_user2.py' script"



assertEquals(exceptedStep1, stepsdescription1)
assertEquals(exceptedStep2, stepsdescription2)
assertEquals(exceptedStep3, stepsdescription3)
assertEquals(exceptedStep4, stepsdescription4)
assertEquals(exceptedStep5, stepsdescription5)


deployit.startTaskAndWait(taskid)
wait_for_task_state(taskid, TaskExecutionState.DONE)

# Cleanup the tasks
undeployTask = deployment.createUndeployTask("Environments/rules-StepPlanEnv/RulesApp")
deployit.startTaskAndWait(undeployTask.id)
repository.delete(yakEnv.id)
repository.delete(yakServer1.id)
repository.delete(myhost.id)
repository.delete("Applications/RulesApp")

