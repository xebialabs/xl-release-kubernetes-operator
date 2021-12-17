from com.xebialabs.deployit.core.api.resteasy import Date
from ai.digital.deploy.sql.model import Report
from java.util import ArrayList
from java.util import Calendar, Locale
from com.xebialabs.deployit.core.util import CiUtils
from org.joda.time import DateTime

begin = DateTime.now().minusHours(2).toCalendar(Locale.getDefault())
# prepare data
shopFrontendApp1 = create_random_application("app-dependencies-ShopFrontend")
shopBackendApp1 = create_random_application("app-dependencies-ShopBackend")
shopServicesApp1 = create_random_application('app-dependencies-ShopServices')
shopDatabaseApp1 = create_random_application('app-dependencies-ShopDatabase')
env = create_random_environment_with_yak_server("env1")

shopFrontendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopFrontendApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopBackendApp1.name: "1.0", shopServicesApp1.name: "1.5"}}))
shopBackendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopBackendApp1.id, 'udm.DeploymentPackage',  {}))
shopServicesPackage_1_5 = repository.create(factory.configurationItem('%s/1.5' % shopServicesApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopDatabaseApp1.name: "[1.0, 3.0]"}}))
shopDatabasePackage_2_0 = repository.create(factory.configurationItem('%s/2.0' % shopDatabaseApp1.id, 'udm.DeploymentPackage', {}))

backendDeployable = repository.create(factory.configurationItem('%s/backendDeployable' % shopBackendPackage_1_0.id, 'yak.YakConfigurationSpec', {}))
frontendDeployable = repository.create(factory.configurationItem('%s/frontendDeployable' % shopFrontendPackage_1_0.id, 'yak.YakConfigurationSpec', {}))
servicesDeployable = repository.create(factory.configurationItem('%s/servicesDeployable' % shopServicesPackage_1_5.id, 'yak.YakConfigurationSpec', {}))
databaseDeployable = repository.create(factory.configurationItem('%s/databaseDeployable' % shopDatabasePackage_2_0.id, 'yak.YakConfigurationSpec', {}))

# prepare deployment
depl = deployment.prepareInitial(shopFrontendPackage_1_0.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)

end = DateTime.now().plusHours(2).toCalendar(Locale.getDefault())
report = proxies.report.getTaskReport(Date(begin), Date(end), None, None, 'none', None, None, None, False, None, ArrayList())
reportLines = filter(lambda x: x.values['taskId'] == taskId, Report.fromLines(report).lines)

assertEquals(1, len(reportLines))
assertEquals("%s/1.0, %s/1.5, %s/1.0, %s/2.0" % (CiUtils.getName(shopFrontendApp1.id), CiUtils.getName(shopServicesApp1.id), CiUtils.getName(shopBackendApp1.id), CiUtils.getName(shopDatabaseApp1.id)), reportLines[0].values['package'])

# Additional parameters in filter search
users = ArrayList()
users.add("admin")
states = ArrayList()
states.add("DONE")
states.add("PENDING")

report = proxies.report.getTaskReport(Date(begin), Date(end), None, None, 'none',
                                      users, states, taskId, False, None, ArrayList())
reportLines = filter(lambda x: x.values['taskId'] == taskId, Report.fromLines(report).lines)

assertEquals(1, len(reportLines))
assertEquals("%s/1.0, %s/1.5, %s/1.0, %s/2.0" % (CiUtils.getName(shopFrontendApp1.id), CiUtils.getName(shopServicesApp1.id), CiUtils.getName(shopBackendApp1.id), CiUtils.getName(shopDatabaseApp1.id)), reportLines[0].values['package'])

#undeploy
undeployTask = deployment.createUndeployTask(depl.deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

undeployTask = deployment.createUndeployTask(depl.requiredDeployments[2].deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

undeployTask = deployment.createUndeployTask(depl.requiredDeployments[1].deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)

undeployTask = deployment.createUndeployTask(depl.requiredDeployments[0].deployedApplication.id)
deployit.startTaskAndWait(undeployTask.id)
