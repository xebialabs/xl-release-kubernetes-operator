### SETUP
host = create_random_host("localhost")
lockManger = create_lockManager("mylockManger")
env = create_random_environment_with_lock("commandEnv", [host.id])

# deploy app which fails command validation
app1 = create_random_application("commandAppLock1")
package1 = repository.create(factory.configurationItem(app1.id + "/1.0", "udm.DeploymentPackage"))
command1 = repository.create(factory.configurationItem(app1.id + "/1.0/command1", "cmd.Command", {"commandLine": "copy"}))


depl1 = deployment.prepareInitial(package1.id, env.id)
depl1 = deployment.prepareAutoDeployeds(depl1)
assertEquals(1, len(depl1.deployeds))
taskId = deployment.createDeployTask(depl1).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.FAILED)


# Control task to listLocks.
control = deployit.prepareControlTask(lockManger, "listLocks")
controlTaskId = deployit.createControlTask(control)
deployit.startTask(controlTaskId)
wait_for_task_state(controlTaskId, TaskExecutionState.EXECUTED)

steps = tasks.steps(controlTaskId).steps
assertEquals(1, len(steps))

print ('test lockManger')
print (steps)
print (steps[0].log)
assertTrue(steps[0].log.find('/Infrastructure/localhost') > -1)
assertTrue(steps[0].log.find('/Environments/commandEnv') > -1)
task2.archive(controlTaskId)

# Control task to clearLocks.
clearLocksControl = deployit.prepareControlTask(lockManger, "clearLocks")
clearLocksControlTaskId = deployit.createControlTask(clearLocksControl)
deployit.startTask(clearLocksControlTaskId)
wait_for_task_state(clearLocksControlTaskId, TaskExecutionState.EXECUTED)
task2.archive(clearLocksControlTaskId)

listLocksControl = deployit.prepareControlTask(lockManger, "listLocks")
listLocksControlTaskId = deployit.createControlTask(listLocksControl)
deployit.startTask(listLocksControlTaskId)
wait_for_task_state(listLocksControlTaskId, TaskExecutionState.EXECUTED)

listLocksSteps = tasks.steps(listLocksControlTaskId).steps
assertEquals(1, len(listLocksSteps))

print (listLocksSteps)
print (listLocksSteps[0].log)
assertTrue(listLocksSteps[0].log.find('none') > -1)
task2.archive(listLocksControlTaskId)

# cleanup
repository.delete(env.id)
repository.delete(host.id)
repository.delete(lockManger.id)
repository.delete(app1.id)