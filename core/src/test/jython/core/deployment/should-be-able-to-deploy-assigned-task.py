prefix = "assigned-task-deployment"
envName = prefix + "-env"
env = create_random_environment_with_yak_server(envName)
package = repository.read("Applications/DeploymentApp/1.0")

# Start deployment as admin
depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

# Admin: assign task to deployment-user
deployit.assignTask(taskId, deploymentUser)

# Login as deployment-user
security.logout()
security.login(deploymentUser, DEFAULT_PASSWORD)

# Deployment-user: start deployment task
deployit.startTaskAndWait(taskId)

# Login as admin
security.logout()
security.login('admin', 'admin')

