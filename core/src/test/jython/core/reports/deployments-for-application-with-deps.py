from com.xebialabs.deployit.core.api.resteasy import Date
from com.xebialabs.deployit.plugin.api.reflect import Type
from com.xebialabs.deployit.engine.api.dto import ConfigurationItemId
from java.util import Calendar, ArrayList

# prepare packages
reportsBackendPackage_1_0 = repository.create(factory.configurationItem(reportsBackendApp.id + '/1.0', 'udm.DeploymentPackage', {}))
reportsFrontendPackage_1_0 = repository.create(factory.configurationItem(reportsFrontendApp.id + '/1.0', 'udm.DeploymentPackage', {
    "applicationDependencies": {reportsBackendApp.name: "[1.0, 1.1]"}
}))

backendDeployable_1_0 = repository.create(factory.configurationItem(reportsBackendPackage_1_0.id + '/backendDeployable1.0', 'yak.YakConfigurationSpec', {}))
frontendDeployable_1_0 = repository.create(factory.configurationItem(reportsFrontendPackage_1_0.id + '/frontendDeployable1.0', 'yak.YakConfigurationSpec', {}))

# deploy frontend and backend
depl = deployment.prepareInitial(reportsFrontendPackage_1_0.id, yakEnv3.id)
depl = deployment.prepareAutoDeployeds(depl)
depl.deployedApplication.values['orchestrator'] = ['sequential-by-dependency']
deployment.validate(depl)
task_id_1 = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(task_id_1)
wait_for_task_state(task_id_1, TaskExecutionState.DONE)

# prepare packages for next steps
reportsBackendPackage_1_1 = repository.create(factory.configurationItem(reportsBackendApp.id + '/1.1', 'udm.DeploymentPackage', {}))
reportsBackendPackage_2_0 = repository.create(factory.configurationItem(reportsBackendApp.id + '/2.0', 'udm.DeploymentPackage', {}))
reportsFrontendPackage_2_0 = repository.create(factory.configurationItem(reportsFrontendApp.id + '/2.0', 'udm.DeploymentPackage', {
    "applicationDependencies": {reportsBackendApp.name: "2.0"}
}))

backendDeployable_1_1 = repository.create(factory.configurationItem(reportsBackendPackage_1_1.id + '/backendDeployable1.1', 'yak.YakConfigurationSpec', {}))
backendDeployable_2_0 = repository.create(factory.configurationItem(reportsBackendPackage_2_0.id + '/backendDeployable2.0', 'yak.YakConfigurationSpec', {}))
frontendDeployable_2_0 = repository.create(factory.configurationItem(reportsFrontendPackage_2_0.id + '/frontendDeployable2.0', 'yak.YakConfigurationSpec', {}))

# deploy just the backend
depl2 = deployment.prepareInitial(reportsBackendPackage_1_1.id, yakEnv3.id)
depl2 = deployment.prepareAutoDeployeds(depl2)
deployment.validate(depl2)
task_id_2 = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(task_id_2)
wait_for_task_state(task_id_2, TaskExecutionState.DONE)

# again deploy frontend and backend
depl3 = deployment.prepareInitial(reportsFrontendPackage_2_0.id, yakEnv3.id)
depl3 = deployment.prepareAutoDeployeds(depl3)
depl3.deployedApplication.values['orchestrator'] = ['sequential-by-dependency']
deployment.validate(depl3)
task_id_3 = deployment.createDeployTask(depl3).id
deployit.startTaskAndWait(task_id_3)
wait_for_task_state(task_id_3, TaskExecutionState.DONE)

# check reports
before = Calendar.getInstance()
before.add(Calendar.MINUTE, -5)
after = Calendar.getInstance()
after.add(Calendar.MINUTE, 5)

statuses = ArrayList()
statuses.add("DONE")

cis1 = ArrayList()
cis1.add(ConfigurationItemId(reportsFrontendApp.id, Type.valueOf("udm.Application")))
cis1.add(ConfigurationItemId(yakEnv3.id, Type.valueOf("udm.Environment")))
report1 = proxies.report.getTaskReport(Date(before), Date(after), None, None, "BOTH", None, statuses, None, True, None, cis1)

cis2 = ArrayList()
cis2.add(ConfigurationItemId(reportsBackendApp.id, Type.valueOf("udm.Application")))
cis2.add(ConfigurationItemId(yakEnv3.id, Type.valueOf("udm.Environment")))
report2 = proxies.report.getTaskReport(Date(before), Date(after), None, None, "BOTH", None, statuses, None, True, None, cis2)

reportLines1 = report1.toArray()
reportLines2 = report2.toArray()
assertEquals(2, len(reportLines1))
assertEquals(3, len(reportLines2))

assertEquals('DONE', reportLines1[0].values["status"])
assertEquals('Update', reportLines1[0].values["type"])
assertEquals('reportsFrontend/2.0, reportsBackend/2.0', reportLines1[0].values["package"])

assertEquals('DONE', reportLines1[1].values["status"])
assertEquals('Initial', reportLines1[1].values["type"])
assertEquals('reportsFrontend/1.0, reportsBackend/1.0', reportLines1[1].values["package"])

assertEquals('DONE', reportLines2[0].values["status"])
assertEquals('Update', reportLines2[0].values["type"])
assertEquals('reportsFrontend/2.0, reportsBackend/2.0', reportLines2[0].values["package"])

assertEquals('DONE', reportLines2[1].values["status"])
assertEquals('Update', reportLines2[1].values["type"])
assertEquals('reportsBackend/1.1', reportLines2[1].values["package"])

assertEquals('DONE', reportLines2[2].values["status"])
assertEquals('Initial', reportLines2[2].values["type"])
assertEquals('reportsFrontend/1.0, reportsBackend/1.0', reportLines2[2].values["package"])
