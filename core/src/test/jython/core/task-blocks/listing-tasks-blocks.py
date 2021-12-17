yakPackage = repository.read("Applications/TaskBlockApp/1.0")

# Start deployment as admin
depl, taskId1 = deploy(yakPackage, yakEnv2)

# Create deployment
switchUser(taskListingUser)
depl2, taskId2 = deploy(yakPackage, yakEnv)

# task-listing-user: List *my* unfinished tasks
tasks = task2.myCurrentTaskSummaries
assertEquals(1, len(tasks), "listUnfinished should only show the users tasks")
taskIds = get_task_ids(tasks)
assertTrue(taskId2 in taskIds)

# task-listing-user: Can't list *all* unfinished tasks
tasks = task2.allCurrentTaskSummaries
taskIds = get_task_ids(tasks)
assertTrue(taskId2 in taskIds)

# Test as user that has deploy#initial on all Environments
switchUser(taskListingUser2)
tasks = task2.allCurrentTaskSummaries
taskIds = get_task_ids(tasks)
assertTrue(taskId2 in taskIds)
assertTrue(taskId1 in taskIds)

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

switchUser('admin')
task2.cancel(taskId1)
task2.cancel(taskId2)
