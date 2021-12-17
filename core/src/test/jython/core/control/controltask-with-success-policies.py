# create a herd of yaks
herd = create_random_host('control-task-herd', 'yak.HerdWithPolicies', {'onSuccessPolicy': 'NOOP'})

# first execute control task with NOOP onSuccessPolicy
control = deployit.prepareControlTask(herd, 'breedHerd')
control.parameters.values['yaksToBreed'] = 5
controlTaskId = deployit.createControlTask(control)
deployit.startTask(controlTaskId)
wait_for_task_state(controlTaskId, TaskExecutionState.EXECUTED)
task2.archive(controlTaskId)

# now with changed onSuccessPolicy to archive
herd.values['onSuccessPolicy'] = 'ARCHIVE'
herd = repository.update(herd)

control = deployit.prepareControlTask(herd, 'breedHerd')
control.parameters.values['yaksToBreed'] = 5
controlTaskId = deployit.createControlTask(control)
deployit.startTask(controlTaskId)
wait_for_task_state(controlTaskId, TaskExecutionState.DONE)

# check reports
wait_for_report_task(controlTaskId)
