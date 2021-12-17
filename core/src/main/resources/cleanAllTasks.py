import time
from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

switchUser('admin')


def cancelOrArchive(task):
    if task.state == TaskExecutionState.EXECUTED:
        task2.archive(task.id)
    else:
        task2.cancel(task.id)


def stopAndWait(task):
    task_id = task.id
    non_executing_states = [TaskExecutionState.DONE, TaskExecutionState.EXECUTED, TaskExecutionState.STOPPED,
                            TaskExecutionState.FAILED, TaskExecutionState.ABORTED]

    if task.state.isExecutingSteps():
        task2.abort(task_id)

        attempt = 0
        while task.state.name() not in non_executing_states:
            attempt += 1
            if attempt > 20:
                raise AssertionError(
                    "Task [" + str(task_id) + "] wasn't aborted during " + str(attempt) + " seconds. Task state is " + task.state.name())
            time.sleep(1)
            task = task2.get(task_id)
            print "task state is " + task.state.name()

    cancelOrArchive(task)


print "****** Cleaning active tasks if present ******"
for task in task2.allCurrentTasksSummaries:
    task2.assign(task.id, 'admin')
    stopAndWait(task)
