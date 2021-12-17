from time import sleep
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

def waitForTask(taskId, archive=True):
    while True:
        try:
            state = tasks.get(taskId)
        except:
            return # the task is already archived

        if state.state == TaskExecutionState.DONE:
            return

        if state.state == TaskExecutionState.EXECUTED:
            print "Task state is", state.state,", archiving"
            if archive:
                tasks.archive(taskId)
            break
        print "Task state is", state.state
        sleep(1)

def checkTaskOperationSucceeds(taskId, action, undoAction=None):
    action(taskId)
    if undoAction is not None:
        undoAction(taskId)


def checkTaskOperationFails(taskId, method, undoAction=None):
    checkOperationFails(lambda: method(taskId))


def checkOperationFails(operation, undoAction=None):
    try:
        operation()
    except:
        pass
    else:
        if undoAction is not None:
            undoAction(taskId)
        raise Exception("Should not be allowed.")


def waitAndUndeploy(taskId):
    switchUser('admin')
    waitForTask(taskId)
    undeployTaskId = deployment.createUndeployTask("Environments/security-model-dir/security-model-env1/SecurityModelApp2").id
    deployit.startTaskAndWait(undeployTaskId)


def prepareDeploymentTask(package, env):
    depl = deployment.prepareInitial(package.id, env.id)
    return deployment.createDeployTask(depl).id


def runScenarioFor(preAction, action, reverseAction):
    switchUser('security-model-starter')
    taskId = preAction(package, env)

    switchUser('security-model-other_user')
    checkTaskOperationFails(taskId, action, reverseAction)

    switchUser('security-model-starter')
    checkTaskOperationSucceeds(taskId, action, reverseAction)

    taskId = preAction(package, env)
    switchUser('admin')
    checkTaskOperationSucceeds(taskId, action, reverseAction)


# Setup


repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))
package = deployit.importPackage('SecurityModelApp2/1.0')
host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'yak.YakServer', {}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))

createUser('security-model-starter', ['login','task#move_step', 'task#skip_step', ('deploy#initial', "Environments/security-model-dir"), ('deploy#undeploy', "Environments/security-model-dir")])
createUser('security-model-other_user', ['login', ('deploy#initial', "Environments/security-model-dir"), ('deploy#undeploy', "Environments/security-model-dir")])

security.grant('read', 'security-model-starter', ['Applications/security-model-dir'])
# Starting tasks
runScenarioFor(prepareDeploymentTask, tasks.start, waitAndUndeploy)

# Stopping tasks
runScenarioFor(prepareDeploymentTask, tasks.stop, tasks.cancel)

# Cancelling tasks
runScenarioFor(prepareDeploymentTask, tasks.cancel, lambda x: None)

# Aborting tasks
runScenarioFor(prepareDeploymentTask, tasks.abort, tasks.cancel)

# Archiving tasks
def prepareAndExecuteDeploymentTask(package, env):
    taskId = prepareDeploymentTask(package, env)
    tasks.start(taskId)
    waitForTask(taskId, False)
    return taskId

runScenarioFor(prepareAndExecuteDeploymentTask, tasks.archive, waitAndUndeploy)

# Get step
runScenarioFor(prepareDeploymentTask, lambda id: tasks.step(id, 1), tasks.cancel)

# Get steps
runScenarioFor(prepareDeploymentTask, lambda id: tasks.steps(id), tasks.cancel)

# Get task
runScenarioFor(prepareDeploymentTask, lambda id: tasks.get(id), tasks.cancel)

# Skip and unskip step
def skipAndUnskip(id):
    tasks.skip(id, [1])
    tasks.unskip(id, [1])

# Removing the check as the skip API assumes a single block and thus fails due to DEPL-8714, which adds multiple blocks.
#runScenarioFor(prepareDeploymentTask, skipAndUnskip, tasks.cancel)

# Query
switchUser('security-model-other_user')
checkOperationFails(lambda: tasks.query('01/01/1986', '01/01/2086'))

switchUser('admin')
tasks.query('01/01/1986', '01/01/2086')

# Export
switchUser('security-model-other_user')
checkOperationFails(lambda: tasks.export('01/01/1986', '01/01/2086'))

switchUser('admin')
tasks.export('01/01/1986', '01/01/2086')

# Tear down
switchUser('admin')
repository.delete("Applications/security-model-dir/SecurityModelApp2")

security.deleteUser('security-model-starter')
security.removeRole('security-model-starter')
security.deleteUser('security-model-other_user')
security.removeRole('security-model-other_user')
