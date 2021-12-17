from com.xebialabs.deployit.core.api.resteasy import Date
from com.xebialabs.deployit.engine.api.dto import ConfigurationItemId
from java.util import Calendar, ArrayList

#user allowed to see reports
security.grant('report#view', 'security-model-user')

# deploy application as admin
repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp-permissions','udm.Application',{}))
package = deployit.importPackage('SecurityModelApp-permissions/1.0')
host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host-permissions", 'yak.YakServer', {}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env-permissions", "udm.Environment", {'members':[host.id]}))
depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

# check reports
before = Calendar.getInstance()
before.add(Calendar.HOUR, -1)
after = Calendar.getInstance()
after.add(Calendar.HOUR, 1)

cis = ArrayList()
cis.add(ConfigurationItemId(env.id, Type.valueOf("udm.Environment")))

#check as admin
report = proxies.report.getTaskReport(Date(before), Date(after), None, None, 'both', None, None, None, False, None, cis)
reportLines = report.toArray()
adminReportNumber = len(reportLines)
assertTrue(adminReportNumber > 0)
assertEquals('SecurityModelApp-permissions/1.0', reportLines[0].values["package"])

# with no permissions to apps or envs the result is empty
switchUser('security-model-user')
report = proxies.report.getTaskReport(Date(before), Date(after), None, None, 'both', None, None, None, False, None, cis)
reportLines = report.toArray()
assertEquals(0, len(reportLines))

# grant permissions to view the apps and envs
switchUser('admin')
security.grant('read', 'security-model-user', ['Environments'])
security.grant('read', 'security-model-user', ['Applications'])
switchUser('security-model-user')

# the result now is same as for admin user
report = proxies.report.getTaskReport(Date(before), Date(after), None, None, 'both', None, None, None, False, None, cis)
reportLines = report.toArray()
assertEquals(adminReportNumber, len(reportLines))
assertEquals('SecurityModelApp-permissions/1.0', reportLines[0].values["package"])

# do the clean-up
switchUser('admin')
security.revoke('read', 'security-model-user', ['Environments/security-model-dir'])
security.revoke('read', 'security-model-user', ['Applications/security-model-dir'])
security.revoke('report#view', 'security-model-user')

repository.delete(env.id)
repository.delete(host.id)
repository.delete(depl.id)
repository.delete(package.id)
