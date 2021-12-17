from org.joda.time import DateTime
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

env = create_random_environment_with_yak_server("env1")
yakPackage = repository.read("Applications/TaskBlockApp/1.0")

depl, taskId = deploy(yakPackage, env)
assertNotNone(taskId)

scheduleAndWait(taskId, DateTime().plusDays(1))
wait_for_task_state(taskId, TaskExecutionState.SCHEDULED)

allTasks = task2.allCurrentTaskSummaries
taskIds = get_task_ids(allTasks)
assertTrue(taskId in taskIds)

### Try to start scheduled task  ###

task2.start(taskId)
deployit.waitForTask(taskId)

wait_for_task_state(taskId, TaskExecutionState.DONE)
allTasks2 = task2.allCurrentTaskSummaries
taskIds2 = get_task_ids(allTasks2)
assertFalse(taskId in taskIds2)
