import urllib2, base64
from xml.etree import ElementTree

package = repository.read("Applications/StepLogApp/1.0.0")
host = repository.create(factory.configurationItem("Infrastructure/stepLog-localHost","overthere.LocalHost",{"os" : os_family() }))
env = repository.create(factory.configurationItem("Environments/stepLog-env", "udm.Environment", {"members": [host.id]}))

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

taskId = deployment.createDeployTask(depl).id

def printStepLog(taskId):
    url = proxies.communicator.config.url + ("/task/%s/step" % taskId)
    print "url: " + url
    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic %s" % base64.b64encode('%s:%s' % ("admin", "admin")))
    steps = ElementTree.fromstring(urllib2.urlopen(request).read()).find('steps')
    for step in steps:
        for item in step:
            if (bool(item.text)):
                print(item.text)
                if ("&#x0" in item.text):
                    fail("Invalid XML characters found.")

try:
    deployit.startTask(taskId)
    printStepLog(taskId)
    wait_for_task_state(taskId, TaskExecutionState.EXECUTED)
    printStepLog(taskId)
    task2.archive(taskId)
    printStepLog(taskId)
finally:
    repository.delete(env.id)
    repository.delete(host.id)
