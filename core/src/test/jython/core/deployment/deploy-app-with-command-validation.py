### SETUP
host = create_random_host("localhost")
env = create_random_environment("commandEnv", [host.id])

# deploy app which passes command validation
app1 = create_random_application("commandApp1")
package1 = repository.create(factory.configurationItem(app1.id + "/1.0", "udm.DeploymentPackage"))
command1 = repository.create(factory.configurationItem(app1.id + "/1.0/command1", "cmd.Command", {"commandLine": "echo hello"}))

depl1 = deployment.prepareInitial(package1.id, env.id)
depl1 = deployment.prepareAutoDeployeds(depl1)
assertEquals(1, len(depl1.deployeds))
taskId = deployment.createDeployTask(depl1).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

# deploy app which fails command validation
# fails due to "restricted-commands": ["^ifconfig.*$"] in deploy-command-whitelist.yaml
app2 = create_random_application("commandApp2")
package2 = repository.create(factory.configurationItem(app2.id + "/1.0", "udm.DeploymentPackage", {"application": app2.id }))
command2 = repository.create(factory.configurationItem(app2.id + "/1.0/command2", "cmd.Command", {"commandLine": "ifconfig"}))

depl2 = deployment.prepareInitial(package2.id, env.id)
depl2 = deployment.prepareAutoDeployeds(depl2)
assertEquals(1, len(depl2.deployeds))
taskId = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.FAILED)

# cleanup
repository.delete(env.id)
repository.delete(host.id)
repository.delete(app1.id)
repository.delete(app2.id)
