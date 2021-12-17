if metadataService is None : raise AssertionError("com.xebialabs.deployit.engine.api.ServiceHolder is not populated")

isCorrectType = False
for d in specification.deltas:
    if(d.deployed is not None and d.deployed.type == "yak.DeployedYakRule" and context.deployedApplication.environment.name == "rules-ScriptPlanEnv"):
        isCorrectType = True
if(isCorrectType):
    step = steps.rule_post_step()
    context.addStep(step)