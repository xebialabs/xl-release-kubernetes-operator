import time
from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

# logs are not available right away, we have an eventual consistency when task is done.
def getLogs(task_id, step_path):
    attempts = 5
    exception = None
    while(attempts > 0):
      print("Left attempt # %s " % attempts)
      try:
         return task2.getStepLog(task_id, step_path)
      except DeployitClientException, e:
        time.sleep(3)
        attempts -=1
        exception = e
    else:
       print(e)

depl = deployment.prepareInitial('Applications/satellite-app/1.0.0', 'Environments/satellite-env')
depl = deployment.prepareAutoDeployeds(depl)
task_id = deployment.createDeployTask(depl).id

try:
    task2.start(task_id)
    wait_for_task_state(task_id, TaskExecutionState.EXECUTED)

    taskStepLog = getLogs(task_id, "0_2_1_1")

    assertTrue('Uploading artifact' in taskStepLog.log())
    assertTrue('Screenshot 2021-10-06 at 17.00.49.png' in taskStepLog.log())
except Exception as e:
    fail(e)
    print(e)
finally:
    undeployTask = deployment.createUndeployTask(depl.deployedApplication.id).id
    task2.start(undeployTask)
    wait_for_task_state(undeployTask, TaskExecutionState.EXECUTED)
