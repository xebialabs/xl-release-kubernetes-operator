isCorrectType = False
for d in specification.deltas:
    if(d.deployed is not None and d.deployed.type == "yak.DeployedYakRule" and  context.deployedApplication.environment.name == "rules-ScriptPlanEnv" ):
        isCorrectType = True
if(isCorrectType):
    step = steps.rule_pre_step(pre_param = "pre-plan")
    context.addStep(step)