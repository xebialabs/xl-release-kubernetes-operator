import base64
import json
import urllib2
import urllib
from com.xebialabs.deployit.core.api.resteasy import Date
# Common utils
reportUrl = "http://localhost:%s/deployit/internal/reports/widgetdata" % _global_integration_test_port

def makeRequest(username, widget, begin, end):
    data = {
        'widgetType': widget,
        'begin': Date(begin),
        'end': Date(end)
    }
    query_params = urllib.urlencode(data)
    url = reportUrl + "?" + query_params
    base64string = base64.encodestring('%s:%s' % (username, DEFAULT_PASSWORD)).replace('\n', '')

    request = urllib2.Request(url)
    request.add_header("Content-Type", "application/json")
    request.add_header("Accept", "application/json")
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)
    return json.loads(response.read())

# Create users
security.createUser("alfa", DEFAULT_PASSWORD)
security.createUser("bravo", DEFAULT_PASSWORD)
security.createUser("charlie", DEFAULT_PASSWORD)

# Assign roles
security.assignRole("alfa", ["alfa"])
security.assignRole("bravo", ["bravo"])
security.assignRole("charlie", ["charlie"])
security.assignRole("delta", ["alfa", "bravo", "charlie"])

# Grant global permissions
security.grant("report#view", "alfa")
security.grant("report#view", "bravo")
security.grant("login", "delta")

# Create folders
appAlfaDir = repository.create(factory.configurationItem('Applications/Alfa', 'core.Directory', {}))
appBravoDir = repository.create(factory.configurationItem('Applications/Bravo', 'core.Directory', {}))
appCharlieDir = repository.create(factory.configurationItem('Applications/Charlie', 'core.Directory', {}))

envAlfaDir = repository.create(factory.configurationItem('Environments/Alfa', 'core.Directory', {}))
envBravoDir = repository.create(factory.configurationItem('Environments/Bravo', 'core.Directory', {}))
envCharlieDir = repository.create(factory.configurationItem('Environments/Charlie', 'core.Directory', {}))

# Grant local permissions
security.grant("read", "alfa", [appAlfaDir.id, appBravoDir.id, appCharlieDir.id])
security.grant("read", "bravo", [appBravoDir.id])
security.grant("read", "charlie", [appCharlieDir.id])

security.grant("read", "alfa", [envAlfaDir.id, envBravoDir.id, envCharlieDir.id])
security.grant("read", "bravo", [envBravoDir.id])

# Create infrastructure
yakServerAlfa = repository.create(factory.configurationItem("Infrastructure/report-alfa", "yak.YakServer", {}))
yakServerBravo = repository.create(factory.configurationItem("Infrastructure/report-bravo", "yak.YakServer", {}))
yakServerCharlie = repository.create(factory.configurationItem("Infrastructure/report-charlie", "yak.YakServer", {}))

# Create environments
yakEnvAlfa = repository.create(factory.configurationItem("Environments/Alfa/report-alfa", "udm.Environment", {"members": [yakServerAlfa.id]}))
yakEnvBravo = repository.create(factory.configurationItem("Environments/Bravo/report-bravo", "udm.Environment", {"members": [yakServerBravo.id]}))
yakEnvCharlie = repository.create(factory.configurationItem("Environments/Charlie/report-charlie", "udm.Environment", {"members": [yakServerCharlie.id]}))

# Create packages
_app = 'DeploymentApp-ForReporting'
_appId = 'Applications/' + _app

def importPackages(appToImport):
    deployit.importPackage(appToImport + '/1.0') #Success app
    deployit.importPackage(appToImport + '/2.0') #Success app
    deployit.importPackage(appToImport + '/3.0') #Success app
    deployit.importPackage(appToImport + '/4.0') #Rollback app
    deployit.importPackage(appToImport + '/5.0') #Fail app

### Alfa app
_alfaApp = _app + '-Alfa'
_alfaImportedApp = _appId + '-Alfa'
_alfaAppId = 'Applications/Alfa/' + _app + '-Alfa'

importPackages(_alfaApp)
repository.move(_alfaImportedApp, _alfaAppId)

yakPackage1Alfa = repository.read(_alfaAppId + '/1.0')
yakPackage2Alfa = repository.read(_alfaAppId + '/2.0')
yakPackage3Alfa = repository.read(_alfaAppId + '/3.0')
yakPackage4Alfa = repository.read(_alfaAppId + '/4.0')
yakPackage5Alfa = repository.read(_alfaAppId + '/5.0')

### Bravo app
_bravoApp = _app + '-Bravo'
_bravoImportedApp = _appId + '-Bravo'
_bravoAppId = 'Applications/Bravo/' + _app + '-Bravo'

importPackages(_bravoApp)
repository.move(_bravoImportedApp, _bravoAppId)

yakPackage1Bravo = repository.read(_bravoAppId + '/1.0')
yakPackage2Bravo = repository.read(_bravoAppId + '/2.0')
yakPackage3Bravo = repository.read(_bravoAppId + '/3.0')
yakPackage4Bravo = repository.read(_bravoAppId + '/4.0')
yakPackage5Bravo = repository.read(_bravoAppId + '/5.0')

### Charlie app
_charlieApp = _app + '-Charlie'
_charlieImportedApp = _appId + '-Charlie'
_charlieAppId = 'Applications/Charlie/' + _app + '-Charlie'

importPackages(_charlieApp)
repository.move(_charlieImportedApp, _charlieAppId)

yakPackage1Charlie = repository.read(_charlieAppId + '/1.0')
yakPackage2Charlie = repository.read(_charlieAppId + '/2.0')
yakPackage3Charlie = repository.read(_charlieAppId + '/3.0')
yakPackage4Charlie = repository.read(_charlieAppId + '/4.0')
yakPackage5Charlie = repository.read(_charlieAppId + '/5.0')

# Deploy applications
def deploy(package, environment, state):
    depl = deployment.prepareInitial(package.id, environment.id)
    depl = deployment.prepareAutoDeployeds(depl)
    task_id = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(task_id)
    wait_for_task_state(task_id, state)
    return task_id

def upgrade(package, deployedApp, state):
    depl = deployment.prepareUpgrade(package.id, deployedApp)
    depl = deployment.prepareAutoDeployeds(depl)
    task_id = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(task_id)
    wait_for_task_state(task_id, state)
    return task_id

def undeploy(deployedApp):
    task_id = deployment.createUndeployTask(deployedApp).id
    deployit.startTaskAndWait(task_id)
    wait_for_task_state(task_id, TaskExecutionState.DONE)
    return task_id

def rollback(taskId):
    task = deployment.createRollbackTask(taskId).id
    deployit.startTaskAndWait(task)
    return task

### Deploy alfa packages
####### (5 success)
####### 2 initial
####### 1 upgrade
####### 2 undeploy
_deployedAppAlfa = yakEnvAlfa.id + '/' + _alfaApp

deploy(yakPackage1Alfa, yakEnvAlfa, TaskExecutionState.DONE)
upgrade(yakPackage2Alfa, _deployedAppAlfa, TaskExecutionState.DONE)
undeploy(_deployedAppAlfa)
deploy(yakPackage3Alfa, yakEnvAlfa, TaskExecutionState.DONE)
undeploy(_deployedAppAlfa)

### Deploy beta packages
####### (2 success)
####### 1 initial
####### 1 undeploy
####### (1 failed)
####### 1 upgrade
_deployedAppBravo = yakEnvBravo.id + '/' + _bravoApp
deploy(yakPackage1Bravo, yakEnvBravo, TaskExecutionState.DONE)
failedTask = upgrade(yakPackage5Bravo, _deployedAppBravo, TaskExecutionState.FAILED)
task2.cancel(failedTask)
undeploy(_deployedAppBravo)

### Deploy charlie packages
####### (2 success)
####### 1 initial
####### 1 undeploy
####### (1 rollback)
####### 1 upgrade
_deployedAppCharlie = yakEnvCharlie.id + '/' + _charlieApp
deploy(yakPackage1Charlie, yakEnvCharlie, TaskExecutionState.DONE)

depl = deployment.prepareUpgrade(yakPackage2Charlie.id, _deployedAppCharlie)
depl = deployment.prepareAutoDeployeds(depl)
task = deployment.createDeployTask(depl).id
task2.start(task)
wait_for_task_state(task, TaskExecutionState.EXECUTED)
rollback(task)

undeploy(_deployedAppCharlie)
