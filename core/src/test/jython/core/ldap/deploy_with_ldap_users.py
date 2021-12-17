
security.logout()

# Login with ldap user gandalf
security.login("gandalf", "gandalf")
env = repository.read("Environments/Env1")
examplePackage = repository.read("Applications/ExampleApp/1.0")

# Deploy ExampleApp/1.0 to Env1 with user yoda
depl = deployment.prepareInitial(examplePackage.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

# Undeploy
undeployTask = deployment.createUndeployTask("Environments/Env1/ExampleApp")
deployit.startTaskAndWait(undeployTask.id)

security.logout()

# Login with ldap user frodo
security.login("frodo", "frodo")

# Try deploying ExampleApp/1.0 to Env1 again with user frodo
try:
    depl = deployment.prepareInitial(examplePackage.id, env.id)
except:
    pass
else:
    fail("Frodo should not be able to use environment Env1")

security.logout()

# Try deploying ExampleApp/1.0 to Env1 again with user sauron
try:
    # Login with ldap user sauron - cannot login ldap-hackers
    security.login("sauron", "sauron")
except:
    pass
else:
    fail("Sauron should not be able to login")

security.logout()

