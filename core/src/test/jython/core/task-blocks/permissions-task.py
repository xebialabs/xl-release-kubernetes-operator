from time import sleep

yakPackage4 = repository.read("Applications/TaskBlockApp/4.0")

def waitForTask(taskId, archive=True):
    while True:
        try:
            state = task2.get(taskId)
        except:
            return # the task is already archived


        if state.state == TaskExecutionState.DONE:
            return

        if state.state == TaskExecutionState.EXECUTED:
            print "Task state is", state.state,", archiving"
            if archive:
                task2.archive(taskId)
            break
        print "Task state is", state.state
        sleep(1)

def checkTaskOperationSucceeds(taskId, action, undoAction=None):
    action(taskId)
    if undoAction is not None:
        undoAction(taskId)


def checkTaskOperationFails(taskId, method):
    checkOperationFails(lambda: method(taskId))


def checkOperationFails(operation, undoAction=None):
    try:
        operation()
    except:
        pass
    else:
        if undoAction is not None:
            undoAction(taskId)
        fail("Should not be allowed.")


def waitAndUndeploy(taskId):
    switchUser('admin')
    waitForTask(taskId)
    undeployTaskId = deployment.createUndeployTask("Environments/task-blocks-dir/task-blocks-env1/TaskBlockApp").id
    deployit.startTaskAndWait(undeployTaskId)


def prepareDeploymentTask():
    depl = deployment.prepareInitial(yakPackage4.id, yakEnv.id)
    return deployment.createDeployTask(depl).id


def runScenarioFor(preAction, action, reverseAction):
    switchUser(starterUser)
    taskId = preAction()

    switchUser(otherUser)
    checkTaskOperationFails(taskId, action)

    switchUser(starterUser)
    checkTaskOperationSucceeds(taskId, action, reverseAction)

    switchUser('admin')
    taskId = preAction()
    checkTaskOperationSucceeds(taskId, action, reverseAction)

# Skip and unskip step
def skipAndUnskip(id):
    task2.skip(id, ["0_1_1_1"])
    task2.unskip(id, ["0_1_1_1"])

# Archiving task2
def prepareAndExecuteDeploymentTask():
    taskId = prepareDeploymentTask()
    task2.start(taskId)
    waitForTask(taskId, False)
    return taskId

security.grant('read', starterUser, ['Applications'])
# Starting task2
runScenarioFor(prepareDeploymentTask, task2.start, waitAndUndeploy)

# Stopping task2
runScenarioFor(prepareDeploymentTask, task2.stop, task2.cancel)

# Cancelling task2
runScenarioFor(prepareDeploymentTask, task2.cancel, lambda x: None)

# Aborting task2
runScenarioFor(prepareDeploymentTask, task2.abort, task2.cancel)

runScenarioFor(prepareAndExecuteDeploymentTask, task2.archive, waitAndUndeploy)

# Get step
runScenarioFor(prepareDeploymentTask, lambda id: task2.step(id, "0_1_1_1"), task2.cancel)

# Get steps
runScenarioFor(prepareDeploymentTask, lambda id: task2.steps(id, "0_1_1"), task2.cancel)

# Get task
runScenarioFor(prepareDeploymentTask, lambda id: task2.get(id), task2.cancel)

# Query
switchUser(otherUser)
checkOperationFails(lambda: task2.query('01/01/1986', '01/01/2086'))

switchUser('admin')
task2.query('01/01/1986', '01/01/2086')

# Export
switchUser(otherUser)
checkOperationFails(lambda: task2.export('01/01/1986', '01/01/2086'))

switchUser('admin')
task2.export('01/01/1986', '01/01/2086')
repository.delete("Applications/task-blocks-dir/TaskBlockApp")
