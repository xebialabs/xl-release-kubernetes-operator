repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))

package = deployit.importPackage('SecurityModelApp2/1.0')
host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'yak.YakServer', {}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))
upgrade = deployit.importPackage('SecurityModelApp2/2.0')

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)

security.grant('read', 'security-model-user', ['Applications/security-model-dir'])

switchUser('security-model-user')

try:
	deployment.prepareUpgrade(upgrade.id, env.id + '/SecurityModelApp2')
except:
	switchUser('admin')
else:
	raise Exception("Should not be allowed to upgrade")

security.grant('deploy#upgrade', 'security-model-user', ['Environments/security-model-dir'])

switchUser('security-model-user')

deploymentId = env.id + '/SecurityModelApp2'
depl = deployment.prepareUpgrade(upgrade.id, deploymentId)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

switchUser('admin')

security.revoke('deploy#upgrade', 'security-model-user', ['Environments/security-model-dir'])

switchUser('security-model-user')

try:
	deployment.prepareUpgrade(package.id, deploymentId)
except:
	switchUser('admin')
else:
	raise Exception("Should not be allowed to upgrade")

switchUser('admin')

security.revoke('read', 'security-model-user', ['Applications/security-model-dir'])
