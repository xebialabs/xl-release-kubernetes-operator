repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))

package = deployit.importPackage('SecurityModelApp2/1.0')
host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'yak.YakServer', {}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))

security.grant('read', 'security-model-user', ['Applications/security-model-dir'])
switchUser('security-model-user')

try:
	deployment.prepareInitial(package.id, env.id)
except:
	switchUser('admin')
else:
	raise Exception("Should not be allowed to initially deploy")

security.grant('deploy#initial', 'security-model-user', ['Environments/security-model-dir'])

switchUser('security-model-user')

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)

wait_for_task_state(taskId, TaskExecutionState.DONE)

switchUser('admin')

security.revoke('deploy#initial', 'security-model-user', ['Environments/security-model-dir'])
taskId = deployment.createUndeployTask(env.id + '/SecurityModelApp2').id
deployit.startTaskAndWait(taskId)

switchUser('security-model-user')

try:
	deployit.prepareInitial(package.id, env.id)
except:
	switchUser('admin')
else:
	raise Exception("Should not be allowed to initially deploy")

security.revoke('read', 'security-model-user', ['Applications/security-model-dir'])
