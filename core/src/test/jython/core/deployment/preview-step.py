env = create_random_environment_with_yak_server("env1")
app = create_random_application("app1")
yakPackage10 = repository.create(factory.configurationItem("%s/10.0" % app.id, "udm.DeploymentPackage"))
repository.create(factory.configurationItem("%s/scriptSpec" % yakPackage10.id, "yak.YakPreviewSpec"))

depl = deployment.prepareInitial(yakPackage10.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

previewBlock = deployment.taskPreviewBlock(depl)
previewSteps = previewBlock.blocks[0].block.steps
assertEquals(1, len(previewSteps))

assertFalse('contents' in previewSteps[0].metadata)

previewStep = deployment.taskPreviewBlock(depl, "0_1_1", 1)

# In test data the first line is terminated with CRLF but we expect it to be returned as LF here
expectedPreview = "10 GOTO 20\n20 PRINTLN \"Hello World\"\n30 PRINTLN \"I'm a stupid Basic Script\""
assertEquals(expectedPreview, previewStep.metadata["contents"])

taskid = deployment.createDeployTask(depl).id

steps = tasks.steps(taskid).steps
assertEquals(2, len(steps))

print steps
print steps[0].metadata

# Once it's a task, we don't automatically return the preview
assertFalse('contents' in steps[0].metadata)

task2.cancel(taskid)
