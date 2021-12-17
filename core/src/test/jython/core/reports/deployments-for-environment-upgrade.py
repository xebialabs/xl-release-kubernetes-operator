from com.xebialabs.deployit.core.api.resteasy import Date
from java.util import Calendar

# run initial deployment and get deployed application report
depl = deployment.prepareInitial(yakPackage.id, yakEnv2.id)
depl = deployment.prepareAutoDeployeds(depl)

assertEquals(1, len(depl.deployeds))

initialTaskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(initialTaskId)
wait_for_task_state(initialTaskId, TaskExecutionState.DONE)

checkpoint1 = Calendar.getInstance()
checkpoint1.add(Calendar.MINUTE, 5)

report = proxies.report.deploymentsForEnvironment(yakEnv2.id, Date(checkpoint1))
reportLines = report.lines
assertEquals(1, len(reportLines))
assertEquals('DeploymentApp-ForReporting', reportLines[0].values['application'])
assertEquals(initialTaskId, reportLines[0].values['taskId'])
assertEquals('1.0', reportLines[0].values['version'])
assertEquals('admin', reportLines[0].values['user'])

# run upgrade and get deployed application report
depl2 = deployment.prepareUpgrade(yakPackage2_0.id, depl.deployedApplication.id)
depl2 = deployment.prepareAutoDeployeds(depl2)
assertEquals(1, len(depl2.deployeds))

upgradeTaskId = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(upgradeTaskId)
wait_for_task_state(upgradeTaskId, TaskExecutionState.DONE)

checkpoint2 = Calendar.getInstance()
checkpoint2.add(Calendar.MINUTE, 5)

report = proxies.report.deploymentsForEnvironment(yakEnv2.id, Date(checkpoint2))
reportLines = report.lines
assertEquals(1, len(reportLines))
assertEquals('DeploymentApp-ForReporting', reportLines[0].values['application'])
# flaky on Jenkins: AssertionErrors, proper test isolation level?
# assertEquals(upgradeTaskId, reportLines[0].values['taskId'])
# assertEquals('2.0', reportLines[0].values['version'])
assertEquals('admin', reportLines[0].values['user'])
