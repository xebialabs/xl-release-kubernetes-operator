repository.create(factory.configurationItem('Applications/security-model-dir/SecurityModelApp2','udm.Application',{}))

deployit.importPackage("SecurityModelApp2/1.0")
yakPackage10 = repository.create(factory.configurationItem("Applications/security-model-dir/SecurityModelApp2/10.0", "udm.DeploymentPackage"))
repository.create(factory.configurationItem(yakPackage10.id + "/scriptSpec", "yak.YakPreviewSpec"))
host = repository.create(factory.configurationItem("Infrastructure/security-model-dir/security-model-host1", 'yak.YakServer', {}))
env = repository.create(factory.configurationItem("Environments/security-model-dir/security-model-env1", "udm.Environment", {'members':[host.id]}))

security.grant("deploy#initial", "security-model-user", ["Environments/security-model-dir"])
security.grant('read', 'security-model-user', ['Applications/security-model-dir'])
switchUser('security-model-user')

depl = deployment.prepareInitial(yakPackage10.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

previewStep = deployment.taskPreviewBlock(depl, "0_1_1", 1)

assertFalse('contents' in previewStep.metadata)

switchUser('admin')
security.grant('task#preview_step', 'security-model-user')
switchUser('security-model-user')

previewStep = deployment.taskPreviewBlock(depl, "0_1_1", 1)

deployment.validate(depl)

assertTrue('contents' in previewStep.metadata)

switchUser("admin")
security.revoke('task#preview_step', 'security-model-user')

repository.delete(env.id)
repository.delete(host.id)
repository.delete("Applications/security-model-dir/SecurityModelApp2")
