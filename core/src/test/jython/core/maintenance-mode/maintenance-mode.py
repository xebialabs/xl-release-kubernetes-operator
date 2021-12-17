from javax.ws.rs import ServiceUnavailableException
from java.lang import RuntimeException

yakServer = repository.create(factory.configurationItem("Infrastructure/rollback-yak1", "yak.YakServer", {}))
yakDirectory = repository.create(factory.configurationItem("Environments/rollback-dir", "core.Directory"))
yakEnv = repository.create(factory.configurationItem("Environments/rollback-dir/rollback-env2", "udm.Environment", {"members": [yakServer.id]}))

taskListingUser = 'maintenance-mode-task-listing-user'
security.createUser(taskListingUser, DEFAULT_PASSWORD)
security.assignRole(taskListingUser, [taskListingUser])
security.grant('login', taskListingUser)
security.grant('read', taskListingUser, ['Applications', 'Environments'])
security.grant('deploy#initial', taskListingUser, [yakDirectory.id])

taskListingUser2 = 'maintenance-mode-task-listing-user2'
security.createUser(taskListingUser2, DEFAULT_PASSWORD)
security.assignRole(taskListingUser2, [taskListingUser2])
security.grant('login', taskListingUser2)
security.grant('read', taskListingUser2, ['Applications', 'Environments'])
security.grant('deploy#initial', taskListingUser2, ['Environments'])
security.grant('deploy#initial', taskListingUser2, [yakDirectory.id])

yakPackage5_0 = deployit.importPackage('MaintenanceModeApp/5.0')

def prepareDeployment():
    depl = deployment.prepareInitial(yakPackage5_0.id, yakEnv.id)
    depl = deployment.prepareAutoDeployeds(depl)
    assertEquals(1, len(depl.deployeds))
    return deployment.createDeployTask(depl).id

def deploySomething(taskId):
    deployit.startTaskAndWait(taskId)
    wait_for_task_state(taskId, TaskExecutionState.DONE)
    assertTrue(repository.exists(yakEnv.id + '/MaintenanceModeApp'))

def undeploySomething():
    taskId2 = deployment.createUndeployTask(yakEnv.id + '/MaintenanceModeApp').id
    deployit.startTaskAndWait(taskId2)
    wait_for_task_state(taskId2, TaskExecutionState.DONE)
    assertFalse(repository.exists(yakEnv.id + '/MaintenanceModeApp'))

# make sure we're in RUNNING state
server = proxies.server
serverState = server.state
assertEquals("RUNNING", serverState.currentMode)

# deploy and undeploy something when server is in RUNNING state
switchUser(taskListingUser2)
taskId = prepareDeployment()
deploySomething(taskId)
switchUser('admin')
undeploySomething()

try:
    # switch to deployment mode
    switchUser('admin')
    server.startMaintenance()
    serverState = server.state
    assertEquals("MAINTENANCE", serverState.currentMode)

    switchUser(taskListingUser2)
    # without admin permissions we should NOT be able to deploy in MAINTENANCE mode
    taskId = prepareDeployment()
    try:
        # check if user is allowed to deploy - should fail
        deploySomething(taskId)
        raise Exception("Deployment should fail in MAINTENANCE mode for user that doesn't have admin permission")
    except ServiceUnavailableException, msg:
        print msg.message
        if ("HTTP 503 Service Unavailable" not in msg.message):
            raise Exception("Exception should contain 'HTTP 503 Service Unavailable' when in maintenance mode")
        task2.cancel(taskId)

    # with admin permissions we should be able to deploy in MAINTENACE mode
    switchUser('admin')
    taskId = prepareDeployment()
    try:
        # check if admin is allowed to deploy - should succeed
        deploySomething(taskId)
    except:
        raise Exception("Admin should be able to deploy in maintenance mode")

finally:
    switchUser('admin')
    server.stopMaintenance()

    repository.delete(yakEnv.id)
    repository.delete(yakDirectory.id)
    repository.delete(yakServer.id)
    repository.delete('Applications/MaintenanceModeApp')

    security.deleteUser(taskListingUser)
    security.removeRole(taskListingUser)
    security.deleteUser(taskListingUser2)
    security.removeRole(taskListingUser2)
