# Start deployment as admin
switchUser(user2)

yakBlockerPackage = repository.read("Applications/TaskBlockApp/1.0-blocker")
depl, taskId = deploy(yakBlockerPackage, yakEnv2)

switchUser("admin")
# Taking over the task
task = task2.takeover(taskId, user2)
assertEquals("admin", task.owner)

switchUser(user2)

should_fail("User user2 should not be able to take over", task2.takeover, taskId, 'admin')

switchUser(taskTakeoverUser)
task = task2.takeover(taskId, 'admin')
assertEquals(taskTakeoverUser, task.owner)

switchUser("admin")
task2.cancel(taskId)
