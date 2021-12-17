repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))

package = deployit.importPackage('SecurityModelApp2/1.0')
host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'yak.YakServer', {}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)

security.grant('read', 'security-model-user', ['Applications/security-model-dir'])

switchUser('security-model-user')

deploymentId = depl.deployedApplication.id

try:
	deployment.createUndeployTask(deploymentId)
except:
	switchUser('admin')
else:
	raise Exception('no permission to undeploy')

security.grant('deploy#undeploy', 'security-model-user', ['Environments/security-model-dir'])

switchUser('security-model-user')

taskId = deployment.createUndeployTask(deploymentId).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

switchUser('admin')

security.revoke('read', 'security-model-user', ['Applications/security-model-dir'])
security.revoke('deploy#undeploy', 'security-model-user', ['Environments/security-model-dir'])
