yakPackage = deployit.importPackage('RulesApp/13.0')

yakServer1 = repository.create(factory.configurationItem("Infrastructure/rules-yakRuleServerToDelete1", "yak.YakServer"))
yakServer2 = repository.create(factory.configurationItem("Infrastructure/rules-yakRuleServerToDelete2", "yak.YakServer"))

yakEnv = repository.create(
    factory.configurationItem("Environments/rules-XmlPlanEnv", "udm.Environment", {"members": [yakServer1.id, yakServer2.id]})
)

depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)
depl.deployedApplication.orchestrator = ['sequential-by-container']
task_id = deployment.createDeployTask(depl).id

task = task2.get(task_id)

assertTrue(task.getBlock().getBlocks()[0].hasSteps())

task2.cancel(task_id)
repository.delete("Applications/RulesApp")
repository.delete(yakEnv.id)
repository.delete(yakServer1.id)
repository.delete(yakServer2.id)
