security.createUser('security-model-overtaker', DEFAULT_PASSWORD)
security.assignRole('security-model-overtaker', ['security-model-overtaker'])
security.grant('login', 'security-model-overtaker')

repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))

deployit.importPackage("SecurityModelApp2/1.0")
yakPackage10 = repository.create(factory.configurationItem("Applications/security-model-dir/SecurityModelApp2/10.0", "udm.DeploymentPackage"))
repository.create(factory.configurationItem(yakPackage10.id + "/scriptSpec", "yak.YakPreviewSpec"))
host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'yak.YakServer', {}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))

security.grant("deploy#initial", "security-model-user", ["Environments/security-model-dir"])
security.grant('read', 'security-model-user', ['Applications/security-model-dir'])
security.grant('task#view', 'security-model-user')

switchUser('security-model-user')

# Setup task
depl = deployment.prepareInitial(yakPackage10.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskid = deployment.createDeployTask(depl).id

# Try takeover
switchUser('security-model-overtaker')
assertEquals(0, len(task2.myCurrentTaskSummaries))

try:
  task2.takeover(taskid, 'security-model-user')
except:
  switchUser('admin')
else:
  raise Exception("Should not be allowed yet.")

# Grant permission and do takeover
security.grant('task#takeover', 'security-model-overtaker', ['Environments/security-model-dir'])
switchUser('security-model-overtaker')

task2.takeover(taskid, 'security-model-user')

assertEquals(1, len(task2.myCurrentTaskSummaries))

# Grant admin to security-model-user and re-takeover
switchUser('admin')
security.revoke('task#takeover', 'security-model-overtaker', ['Environments/security-model-dir'])
security.grant('admin', 'security-model-user')

switchUser("security-model-user")
task2.takeover(taskid, 'security-model-overtaker')

# Cleanup task
task2.cancel(taskid)

# Cleanup security
switchUser("admin")
security.revoke('admin', 'security-model-user')
security.revoke('task#view', 'security-model-user')
security.revoke('login', 'security-model-overtaker')
security.assignRole('security-model-overtaker', [])
security.deleteUser('security-model-overtaker')
security.removeRole('security-model-overtaker')

repository.delete(env.id)
repository.delete(host.id)
repository.delete("Applications/security-model-dir/SecurityModelApp2")
