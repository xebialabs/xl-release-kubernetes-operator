from org.joda.time import DateTime
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

deployedYakFile = factory.configurationItem(yakServer.id + '/test.yak', 'yak.DeployedYakFile', {'deployable':'Applications/ScheduleApp/1.0/test.yak','container':yakServer.id})
depl = deployment.prepareInitial(yakBlockerPackage.id, yakEnv.id)
depl.deployeds = [deployedYakFile]
taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

scheduleAndWait(taskId, DateTime().plusDays(1))

wait_for_task_state(taskId, TaskExecutionState.SCHEDULED)

allTasks = task2.allCurrentTaskSummaries
taskIds = get_task_ids(allTasks)
# check if the task is listed
assertTrue(taskId in taskIds)

### Try to start scheduled task  ###
task2.start(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)

### Check if the scheduled task will finish ###
deployit.waitForTask(taskId)

wait_for_task_state(taskId, TaskExecutionState.DONE)

allTasks2 = task2.allCurrentTaskSummaries
taskIds2 = get_task_ids(allTasks2)
# Task should not be listed any more
assertFalse(taskId in taskIds2)

### Check if the deployment was successful ###

deployedTestYak = repository.read('Infrastructure/schedule-yak1/test.yak')
assertNotNone(deployedTestYak)

deployedYakApp = repository.read(yakEnv.id+'/ScheduleApp')
assertNotNone(deployedYakApp)

