from time import sleep
#
# The getArchivedTaskList() function always returns an empty task list if there are no tasks in repository
# If there is a task, this task will always return at least an empty step list
# Finally, the test data has been setup to contain at least 4 tasks

taskListForThisTest = []
triesLeft = 5
while triesLeft > 0:
    archivedTasks = repository.getArchivedTaskList()
    assertNotNone(archivedTasks)
    taskList = [t for t in archivedTasks if 'application' in t.metadata and str(t.metadata['application']).find('Export') > 0]
    assertNotNone(taskList)
    taskListForThisTest = []
    for t in taskList:
        if t.id in archiveTaskIds:
            taskListForThisTest.append(t)
    if len(taskListForThisTest) < 4:
        triesLeft -= 1
        sleep(.2)
    else:
        triesLeft = -1

assertTrue(len(taskListForThisTest) >= 4)

for t in taskListForThisTest:

    step_blocks = t.get_step_blocks()
    assertNotNone(step_blocks)
    assertEquals(2, len(step_blocks))

    for step_block in step_blocks:
        # checks for the application or the last step of any application (RepositoryUpdateStep)
        if t.metadata['application'] == 'export-tinyExportApp' or step_block == step_blocks[-1]:
            assertEquals(1, len(step_block.getSteps()))
        else:
            assertEquals(2, len(step_block.getSteps()))
        assertEquals("DONE", str(step_block.getState()))

    assertTrue(t.metadata['application'] in ['export-tinyExportApp', 'export-smallExportApp'])
