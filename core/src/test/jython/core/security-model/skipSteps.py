repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))

yakBlockerPackage = deployit.importPackage('SecurityModelApp2/1.0-blocker')
yakServer = repository.create(factory.configurationItem("Infrastructure/security-model-dir/yak1", "yak.YakServer", {}))
yakEnv = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env", "udm.Environment", {"members": [yakServer.id]}))

security.grant('deploy#initial','security-model-user',['Environments/security-model-dir'])
security.grant('read', 'security-model-user', ['Applications/security-model-dir'])
switchUser('security-model-user')

depl = deployment.prepareInitial(yakBlockerPackage.id, yakEnv.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

try:
	deployit.skipSteps(taskId, [1])
except:
	switchUser('admin')
else:
	raise Exception("Should not be allowed (yet)")

security.grant('task#skip_step','security-model-user',['Environments/security-model-dir'])

switchUser('security-model-user')
deployit.skipSteps(taskId, [1])
deployit.cancelTask(taskId)

switchUser('admin')
security.revoke('task#skip_step','security-model-user',['Environments/security-model-dir'])
security.revoke('deploy#initial','security-model-user',['Environments/security-model-dir'])

repository.delete(yakEnv.id)
repository.delete('Infrastructure/security-model-dir/yak1')
repository.delete('Applications/security-model-dir/SecurityModelApp2')