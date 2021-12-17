herd = create_random_host('control-task-herd', 'yak.Herd', {})

control = deployit.prepareControlTask(herd, "breedHerd")

control.parameters.values['yaksToBreed'] = 0
try:
    taskId = deployit.createControlTask(control)
except:
    control.parameters.values['yaksToBreed'] = 5
else:
    raise Exception("Should have validation error")

taskId = deployit.createControlTask(control)

task = tasks.steps(taskId)

assertEquals(5, len(task.steps))

task2.cancel(taskId)
