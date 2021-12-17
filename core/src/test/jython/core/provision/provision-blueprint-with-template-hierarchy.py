from com.xebialabs.deployit.engine.api.execution import TaskExecutionState
from xld_tasks import wait_for_task_state, start_task, archive_task
repository.update(pck4)
pkg = repository.read(pck4.id)
provision = deployment.prepareInitial(pkg.id, provisioning_environment.id)
print "provision package {0}".format(pkg.id)

provision = deployment.prepareAutoDeployeds(provision)
taskId = deployment.createDeployTask(provision).id
start_task(taskId)
wait_for_task_state(taskId, TaskExecutionState.EXECUTED)
assert_exists("Infrastructure/TomcatHost")
assert_exists("Infrastructure/TomcatHost/TomcatServer")

rollback_task_id = deployment.createRollbackTask(taskId).id
start_task(rollback_task_id)
wait_for_task_state(rollback_task_id, TaskExecutionState.EXECUTED)
assert_not_exists("Infrastructure/TomcatHost")
assert_not_exists("Infrastructure/TomcatHost/TomcatServer")

archive_task(rollback_task_id)