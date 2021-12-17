# deploy application as admin
repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))
package = deployit.importPackage('SecurityModelApp2/1.0')
host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'yak.YakServer', {}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))
depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

# Check if admin can view task
wait_for_report_task(taskId)

# User should not be able to view task
switchUser('security-model-user')
try:
    task = proxies.report.getTask(taskId)
    print("task object: %s", task)
except:
    pass
else:
    raise Exception("Should not be allowed to read task info")

# Grant access to user
switchUser('admin')
security.grant('report#view', 'security-model-user')

# User should not be able to read task without read rights
switchUser('security-model-user')
try:
    task = proxies.report.getTask(taskId)
except:
    pass
else:
    raise Exception("Should not be allowed to read task info without read rights")

# Now it should work
switchUser('admin')
security.grant('read', 'security-model-user', ["Environments/security-model-dir"])
security.grant('read', 'security-model-user', ["Applications/security-model-dir"])

switchUser('security-model-user')
try:
    task = proxies.report.getTask(taskId)
    assertNotNone(task)
except:
    raise Exception("Should be allowed to read task info")

# Cleaning everything
switchUser('admin')
security.revoke('report#view', 'security-model-user')

repository.delete(env.id)
repository.delete(host.id)
repository.delete(depl.id)
repository.delete(package.id)
