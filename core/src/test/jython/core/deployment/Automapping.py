from com.xebialabs.deployit.engine.api.execution import TaskExecutionState

# Test 1:Added the new package with Tags in it.

yakTagPackage1 = repository.read('Applications/DeploymentApp/6.0')

# creating env with and without tags

yakServerTag1 = create_random_yak_server("yakTag1", { "tags": ['tag1']})
yakServerNoTag = create_random_yak_server("yakNoTag")
yakServerTag2 = create_random_yak_server("yakTag2", { "tags": ['tag2']})

yakTagEnv = create_random_environment("env1", [yakServerTag1.id, yakServerNoTag.id, yakServerTag2.id])

depl = deployment.prepareInitial(yakTagPackage1.id, yakTagEnv.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)

map = {}
for d in depl.deployeds:
    map[d.id] = d

taskId = deployment.createDeployTask(depl).id
deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

# Test 2: Update the Package version having new Application and deleted Tag from YakServer1

yakTagEnv = repository.read(yakTagEnv.id)

yakServerTag1.values['tags'] = []
repository.update(yakServerTag1)


yakTagPackage2 = repository.read('Applications/DeploymentApp/7.0')

depl2 = deployment.prepareUpgrade(yakTagPackage2.id, '%s/DeploymentApp' % yakTagEnv.id)
depl2 = deployment.prepareAutoDeployeds(depl2)

umap = {}
for d in depl2.deployeds:
    umap[d.id] = d
utaskid = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(utaskid)
wait_for_task_state(utaskid, TaskExecutionState.DONE)
