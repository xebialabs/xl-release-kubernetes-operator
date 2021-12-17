from time import sleep
from org.joda.time import DateTime, DateTimeZone
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState
from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

deployedYakFile = factory.configurationItem(yakServer.id + '/test.yak', 'yak.DeployedYakFile', {'deployable':'Applications/ScheduleApp/1.0/test.yak','container':yakServer.id})
depl = deployment.prepareInitial(yakBlockerPackage.id, yakEnv.id)
depl.deployeds = [deployedYakFile]
taskId = deployment.createDeployTask(depl).id
assertNotNone(taskId)

### Try to schedule a task in the past ###
try:
    scheduleAndWait(taskId, DateTime().minusSeconds(1))
except DeployitClientException, err:
    assertTrue(err.message.find("Cannot schedule a task for the past") > -1, "Message of exception is not correct")
else:
    raise Exception("Should not schedule deployment in past")


### Try to schedule a task in the future ###
try:
    scheduleAndWait(taskId, DateTime().plusDays(365))
except DeployitClientException, e:
    assertTrue(e.message.find("because it is too far into the future") > -1, "Message of exception is not correct")
else:
    raise Exception("Tasks should not be schedulable a year into the future")


originalDate = DateTime()
### Try to schedule a task ###
scheduledDate1 = originalDate.plusSeconds(5)
scheduleAndWait(taskId, scheduledDate1)
retrievedDate1 = task2.get(taskId).scheduledDate
assertEquals(scheduledDate1.withZone(DateTimeZone.UTC), retrievedDate1)
allTasks1 = task2.allCurrentTaskSummaries
taskIds1 = get_task_ids(allTasks1)
# check if the task is listed
assertTrue(taskId in taskIds1)

### Try to re-schedule a task  ###
scheduledDate2 = originalDate.plusSeconds(10)
task2.schedule(taskId, scheduledDate2)
expectedDate2 = scheduledDate2.withZone(DateTimeZone.UTC)
triesLeft = 5
while triesLeft > 0:
    retrievedDate2 = task2.get(taskId).scheduledDate
    if not retrievedDate2.equals(expectedDate2):
        triesLeft -= 1
        sleep(.2)
    else:
        triesLeft = -1

assertEquals(expectedDate2, retrievedDate2)

allTasks2 = task2.allCurrentTaskSummaries
taskIds2 = get_task_ids(allTasks2)
# after rescheduling only one task should be listed
assertTrue(taskId in taskIds2)

### Check if the scheduled task will finish ###
deployit.waitForTask(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

### Check if the deployment was successful ###
deployedTestYak = repository.read('Infrastructure/schedule-yak1/test.yak')
assertNotNone(deployedTestYak)

deployedYakApp = repository.read(yakEnv.id+'/ScheduleApp')
assertNotNone(deployedYakApp)
