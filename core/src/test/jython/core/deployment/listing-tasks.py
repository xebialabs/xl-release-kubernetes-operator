env1 = create_random_environment_with_yak_server("env1")
env2 = create_random_environment_with_yak_server("deployment-dir/env2")
package = repository.read("Applications/DeploymentApp/1.0-blocker")

# Start deployment as admin
depl = deployment.prepareInitial(package.id, env1.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId1 = deployment.createDeployTask(depl).id

switchUser(taskListingUser)

# Create deployment
depl = deployment.prepareInitial(package.id, env2.id)
depl = deployment.prepareAutoDeployeds(depl)
taskId2 = deployment.createDeployTask(depl).id

# task-listing-user: List *my* unfinished tasks
tasks = task2.myCurrentTaskSummaries
assertEquals(1, len(tasks), "listUnfinished should only show the users tasks")

# task-listing-user: Can't list *all* unfinished tasks
tasks = task2.allCurrentTaskSummaries
taskIds = get_task_ids(tasks)
assertTrue(taskId2 in taskIds)

# Test as user that has deploy#initial on all Environments
switchUser(taskListingUser2)
tasks = task2.allCurrentTaskSummaries
# deployment-task-listing-user2 should see all tasks because he has deploy#initial on Environments")
taskIds = get_task_ids(tasks)
assertTrue(taskId1 in taskIds)
assertTrue(taskId2 in taskIds)

# Test as admin
switchUser('admin')

# Admin: List *my* unfinished tasks
tasks = task2.myCurrentTaskSummaries
taskIds = get_task_ids(tasks)
assertTrue(taskId1 in taskIds)

# Admin: List *all* unfinished tasks
tasks = task2.allCurrentTaskSummaries
taskIds = get_task_ids(tasks)
assertTrue(taskId1 in taskIds)
assertTrue(taskId2 in taskIds)

# Cleanup admin tasks
deployit.cancelTask(taskId1)
deployit.cancelTask(taskId2)
