# create a herd of yaks
herd = create_random_host('control-task-herd', 'yak.HerdWithPolicies', {'onFailurePolicy': 'NOOP', 'doKillingStampede': 'true'})

# first execute control task with NOOP onSuccessPolicy
control = deployit.prepareControlTask(herd, 'breedHerd')
control.parameters.values['yaksToBreed'] = 5
controlTaskId = deployit.createControlTask(control)
deployit.startTask(controlTaskId)
wait_for_task_state(controlTaskId, TaskExecutionState.FAILED)
task2.cancel(controlTaskId)

# now with changed onSuccessPolicy to archive
herd.values['onFailurePolicy'] = 'CANCEL_AND_ARCHIVE'
herd = repository.update(herd)

control = deployit.prepareControlTask(herd, 'breedHerd')
control.parameters.values['yaksToBreed'] = 5
autoControlTaskId = deployit.createControlTask(control)
deployit.startTask(autoControlTaskId)

# it's not always cancelled, can also be archived at this time. Has to be handled properly
wait_for_task_state(autoControlTaskId, TaskExecutionState.CANCELLED)

# check reports
wait_for_report_task(autoControlTaskId)
