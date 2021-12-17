env = create_random_environment_with_yak_server("env1")
yakBlockerPackage = repository.read("Applications/TaskBlockApp/1.0-blocker")

# Start deployment as admin
depl, taskId = deploy(yakBlockerPackage, env)

# Admin: assign task to user2
task2.assign(taskId, user2)

# Test as user2
switchUser(user2)

# User2: should have 1 unfinished task
tasks = task2.myCurrentTaskSummaries
assertEquals(1, len(tasks))
taskIds = get_task_ids(tasks)
assertTrue(taskId in taskIds)

# User2: Can't assign task
should_fail("assignTask should only be available to users with perm ADMIN or TASK_ASSIGN", task2.assign, taskId, taskAssigningUser)

# Test as admin
switchUser('admin')
# Admin should be able to assign someone else's task to task-assigning-user
task2.assign(taskId, taskAssigningUser)

# Test as task-assigning-user
switchUser(taskAssigningUser)

# Task assigning user: assign my task to user2
task2.assign(taskId, user2)

# Task assigning user should not assign task someone else's task
should_fail("assignTask should not be allowed with someone else's task", task2.assign, taskId, 'admin')

switchUser('admin')
task2.cancel(taskId)
