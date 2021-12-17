env = create_random_environment_with_yak_server("env1")
package = repository.read("Applications/DeploymentApp/1.0-blocker")

# Start deployment as admin
depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId = deployment.createDeployTask(depl).id

# Admin: assign task to user2
deployit.assignTask(taskId, deploymentUser)

# Test as user2
security.logout()
security.login(deploymentUser, DEFAULT_PASSWORD)

# User2: should have 1 unfinished task
tasks = task2.myCurrentTaskSummaries
assertEquals(1, len(tasks))

# User2: Can't assign task
try:
    deployit.assignTask(taskId, taskAssigningUser)
except:
    pass
else:
    raise Exception("assignTask should only be available to users with perm ADMIN or TASK_ASSIGN")


# Test as admin
security.logout()
security.login('admin', 'admin')

# Admin: assign someone else's task to task-assigning-user
deployit.assignTask(taskId, taskAssigningUser)

# Test as task-assigning-user
security.logout()
security.login(taskAssigningUser, DEFAULT_PASSWORD)

# Task assigning user: assign my task to user2
deployit.assignTask(taskId, deploymentUser)

# Task assigning user: Can't assign task someone else's task
try:
    deployit.assignTask(taskId, 'admin')
except:
    pass
else:
    raise Exception("assignTask should not be allowed with someone else's task")

# Cleanup
# Admin: assign task back to me, then cancel it
security.logout()
security.login('admin', 'admin')

deployit.assignTask(taskId, 'admin')
deployit.cancelTask(taskId)
