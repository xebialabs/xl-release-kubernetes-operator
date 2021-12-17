security.createUser('security-model-upgrader-user', DEFAULT_PASSWORD)
security.assignRole('security-model-upgrader-user', ['security-model-upgrader-user'])
security.grant('login', 'security-model-upgrader-user')

repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))

yakServer = repository.create(factory.configurationItem("Infrastructure/security-model-dir/yakServer", "yak.YakServer", {}))
yakEnv = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env", "udm.Environment", {"members": [yakServer.id]}))


yakPackage1 = deployit.importPackage('SecurityModelApp2/1.0-with-3-yaks')
yakPackage2 = deployit.importPackage('SecurityModelApp2/2.0-with-3-yaks')

depl = deployment.prepareInitial(yakPackage1.id, yakEnv.id)
twoDeployeds = deployment.generateSelectedDeployeds([yakPackage1.id + '/yak1', yakPackage1.id + '/yak2'], depl).deployeds
assertEquals(2, len(twoDeployeds))
depl.deployeds = twoDeployeds

taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

security.grant('read', 'security-model-upgrader-user', ['Applications/security-model-dir'])
security.grant('deploy#upgrade', 'security-model-upgrader-user', ['Environments/security-model-dir'])
switchUser('security-model-upgrader-user')

deploymentId = yakEnv.id + '/SecurityModelApp2'
depl2 = deployment.prepareUpgrade(yakPackage2.id, deploymentId)
upgradedTwoDeployeds = depl2.deployeds
print 'upgraded deployeds: %s' %(upgradedTwoDeployeds)
assertEquals(2, len(upgradedTwoDeployeds))

try:
    deployment.generateSingleDeployed(yakPackage2.id + '/yak3', yakServer.id, 'yak.YakFile', depl2).deployeds
    raise Exception("Should not be allowed to generate new deployeds")
except:
    print 'Fine, security-model-upgrader-user is not allowed to generate any new deployeds'

switchUser('admin')

security.logout()
security.login("admin", "admin")

security.deleteUser("security-model-upgrader-user")
security.revoke('login', 'security-model-upgrader-user')
security.removeRole('security-model-upgrader-user')
