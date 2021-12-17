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

### Try to cancel the scheduled task  ###

deployit.cancelTask(taskId)
allTasks2 = task2.allCurrentTaskSummaries
taskIds2 = get_task_ids(allTasks2)
# check if the task is removed
assertFalse(taskId in taskIds2)
