from org.joda.time import DateTime
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

env = create_random_environment_with_yak_server("env1")
yakBlockerPackage = repository.read("Applications/TaskBlockApp/1.0-blocker")

depl, taskId = deploy(yakBlockerPackage, env)
assertNotNone(taskId)

scheduleAndWait(taskId, DateTime().plusDays(1))
wait_for_task_state(taskId, TaskExecutionState.SCHEDULED)

allTasks = task2.allCurrentTaskSummaries
taskIds = get_task_ids(allTasks)
assertTrue(taskId in taskIds)

### Try to cancel the scheduled task  ###

task2.cancel(taskId)
allTasks2 = task2.allCurrentTaskSummaries
taskIds2 = get_task_ids(allTasks2)
assertFalse(taskId in taskIds2)
