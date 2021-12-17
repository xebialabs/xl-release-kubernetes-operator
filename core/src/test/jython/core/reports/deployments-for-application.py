from com.xebialabs.deployit.core.api.resteasy import Date
from com.xebialabs.deployit.plugin.api.reflect import Type
from com.xebialabs.deployit.engine.api.dto import ConfigurationItemId
from java.util import Calendar, ArrayList

# run initial deployment
depl = deployment.prepareInitial(yakPackage.id, yakEnv3.id)
depl = deployment.prepareAutoDeployeds(depl)
initialTaskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(initialTaskId)
wait_for_task_state(initialTaskId, TaskExecutionState.DONE)

# run upgrade
depl2 = deployment.prepareUpgrade(yakPackage2_0.id, depl.deployedApplication.id)
depl2 = deployment.prepareAutoDeployeds(depl2)
assertEquals(1, len(depl2.deployeds))
upgradeTaskId = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(upgradeTaskId)
wait_for_task_state(initialTaskId, TaskExecutionState.DONE)

# another upgrade
depl3 = deployment.prepareUpgrade(yakPackage3_0.id, depl2.deployedApplication.id)
depl3 = deployment.prepareAutoDeployeds(depl3)
upgradeTaskId2 = deployment.createDeployTask(depl3).id
task2.start(upgradeTaskId2)
wait_for_task_state(upgradeTaskId2, TaskExecutionState.EXECUTED)

# rollback the upgrade
rollbackTaskId = deployment.createRollbackTask(upgradeTaskId2).id
deployit.startTaskAndWait(rollbackTaskId)
wait_for_task_state(rollbackTaskId, TaskExecutionState.DONE)

# run upgrade again
depl4 = deployment.prepareUpgrade(yakPackage3_0.id, depl.deployedApplication.id)
depl4 = deployment.prepareAutoDeployeds(depl4)
assertEquals(1, len(depl4.deployeds))
upgradeTaskId3 = deployment.createDeployTask(depl4).id
deployit.startTaskAndWait(upgradeTaskId3)
wait_for_task_state(upgradeTaskId3, TaskExecutionState.DONE)

# run undeploy
taskId2 = deployment.createUndeployTask(yakEnv3.id + '/DeploymentApp-ForReporting').id
deployit.startTaskAndWait(taskId2)
wait_for_task_state(taskId2, TaskExecutionState.DONE)
assertFalse(repository.exists(yakEnv3.id + '/DeploymentApp-ForReporting'))

# Report should have additional upgrade and undeploy but not rollback
before = Calendar.getInstance()
before.add(Calendar.MINUTE, -5)
after = Calendar.getInstance()
after.add(Calendar.MINUTE, 5)

statuses = ArrayList()
statuses.add("DONE")

cis = ArrayList()
cis.add(ConfigurationItemId('DeploymentApp-ForReporting', Type.valueOf("udm.Application")))
cis.add(ConfigurationItemId(yakEnv3.id, Type.valueOf("udm.Environment")))
report = proxies.report.getTaskReport(Date(before), Date(after), None, None, "BOTH", None, statuses, None, True, None, cis)
reportLines = report.toArray()

assertEquals(4, len(reportLines))

assertEquals('DONE', reportLines[0].values["status"])
assertEquals('Undeployment', reportLines[0].values["type"])
assertEquals('DeploymentApp-ForReporting/3.0', reportLines[0].values["package"])

assertEquals('DONE', reportLines[1].values["status"])
assertEquals('Update', reportLines[1].values["type"])
assertEquals('DeploymentApp-ForReporting/3.0', reportLines[1].values["package"])

assertEquals('DONE', reportLines[2].values["status"])
assertEquals('Update', reportLines[2].values["type"])
assertEquals('DeploymentApp-ForReporting/2.0', reportLines[2].values["package"])

assertEquals('DONE', reportLines[3].values["status"])
assertEquals('Initial', reportLines[3].values["type"])
assertEquals('DeploymentApp-ForReporting/1.0', reportLines[3].values["package"])
