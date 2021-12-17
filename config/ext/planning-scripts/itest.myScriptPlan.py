isCorrectType = False
for d in deltas.deltas:
    if(d.deployed is not None and d.deployed.type == "yak.DeployedYakRule" and context.deployedApplication.environment.name == "rules-ScriptPlanEnv"):
        isCorrectType = True
if(isCorrectType):
    step = steps.rule_plan_step()
    context.addStep(step)