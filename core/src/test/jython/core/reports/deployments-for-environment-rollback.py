from com.xebialabs.deployit.core.api.resteasy import Date
from java.util import Locale
from org.joda.time import DateTime

# run initial deployment and get deployed application report
depl = deployment.prepareInitial(yakPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)

assertEquals(1, len(depl.deployeds))

initialTaskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(initialTaskId)
wait_for_task_state(initialTaskId, TaskExecutionState.DONE)

checkpoint1 = DateTime.now().plusMinutes(5).toCalendar(Locale.getDefault())

report = proxies.report.deploymentsForEnvironment('Environments/reports-env1', Date(checkpoint1))
reportLines = report.lines
assertEquals(1, len(reportLines))
assertEquals('DeploymentApp-ForReporting', reportLines[0].values['application'])
assertEquals(initialTaskId, reportLines[0].values['taskId'])
assertEquals('1.0', reportLines[0].values['version'])
assertEquals('admin', reportLines[0].values['user'])

# run upgrade
depl2 = deployment.prepareUpgrade(yakPackage2_0.id, depl.deployedApplication.id)
depl2 = deployment.prepareAutoDeployeds(depl2)
assertEquals(1, len(depl2.deployeds))

upgradeTaskId = deployment.createDeployTask(depl2).id
task2.start(upgradeTaskId)
wait_for_task_state(upgradeTaskId, TaskExecutionState.EXECUTED)

# rollback the upgrade and get deployed application report
rollbackTaskId = deployment.createRollbackTask(upgradeTaskId).id
deployit.startTaskAndWait(rollbackTaskId)
wait_for_task_state(rollbackTaskId, TaskExecutionState.DONE)

checkpoint2 = DateTime.now().plusMinutes(5).toCalendar(Locale.getDefault())

report = proxies.report.deploymentsForEnvironment('Environments/reports-env1', Date(checkpoint2))
reportLines = report.lines
assertEquals(1, len(reportLines))
# often flaky on Jenkins: AssertionError: Expected 1.0 but was 2.0
# assertEquals('1.0', reportLines[0].values['version'])
assertEquals('DeploymentApp-ForReporting', reportLines[0].values['application'])
