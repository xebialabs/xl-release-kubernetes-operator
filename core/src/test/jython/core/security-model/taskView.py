from com.xebialabs.deployit.engine.api.execution import TaskExecutionState,StepExecutionState
from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2', 'udm.Application', {}))

deployit.importPackage("SecurityModelApp2/1.0")
yakPackage10 = repository.create(
    factory.configurationItem("Applications/security-model-dir/SecurityModelApp2/10.0", "udm.DeploymentPackage"))
repository.create(factory.configurationItem(yakPackage10.id + "/scriptSpec", "yak.YakPreviewSpec"))
host = repository.create(
    factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'yak.YakServer', {}))
env = repository.create(
    factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment",
                              {'members': [host.id]}))

security.grant("deploy#initial", "security-model-user", ["Environments/security-model-dir"])
security.grant('read', 'security-model-user', ['Applications/security-model-dir'])
createUser('security-model-other_user', ['login'])
switchUser('security-model-user')

depl = deployment.prepareInitial(yakPackage10.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

taskid = deployment.createDeployTask(depl).id
wait_for_task_state(taskid, TaskExecutionState.PENDING)

switchUser('security-model-other_user')

try:
    myTask = task2.get(taskid)
    assertEquals('security-model-user', myTask.owner)
except DeployitClientException, e:
    assertEquals(
        'com.xebialabs.deployit.security.PermissionDeniedException [/tasks/v2/{task}]: '
        'Only user with task#view permission or owner or ADMIN can access the task'.format(task=taskid),
        e.message)

try:
    task2.block(taskid, "0_1_1")
except DeployitClientException, e:
    assertEquals(
        'com.xebialabs.deployit.security.PermissionDeniedException [/tasks/v2/{task}/block/0_1_1]: '
        'Only user with task#view permission or owner or ADMIN can access the task'.format(task=taskid),
        e.message)

try:
    task2.steps(taskid, "0_1_1")
except DeployitClientException, e:
    assertEquals(
        'com.xebialabs.deployit.security.PermissionDeniedException [/tasks/v2/{task}/block/0_1_1/step]: '
        'Only user with task#view permission or owner or ADMIN can access the task'.format(task=taskid),
        e.message)

try:
    task2.step(taskid, "0_1_1_1")
except DeployitClientException, e:
    assertEquals(
        'com.xebialabs.deployit.security.PermissionDeniedException [/tasks/v2/{task}/step/0_1_1_1]: '
        'Only user with task#view permission or owner or ADMIN can access the task'.format(task=taskid),
        e.message)

switchUser('admin')
wait_for_task_state(taskid, TaskExecutionState.PENDING)

security.grant('task#view', 'security-model-other_user')
switchUser('security-model-other_user')

wait_for_task_state(taskid, TaskExecutionState.PENDING)

assertTrue(task2.block(taskid, "0_1_1").hasSteps())
assertEquals(1, len(task2.steps(taskid, "0_1_1").getSteps()))
assertStepState(taskid, "0_1_1_1", StepExecutionState.PENDING)

switchUser("admin")

task2.cancel(taskid)

security.revoke('task#view', 'security-model-other_user')
security.deleteUser('security-model-other_user')

repository.delete(env.id)
repository.delete(host.id)
repository.delete("Applications/security-model-dir/SecurityModelApp2")
