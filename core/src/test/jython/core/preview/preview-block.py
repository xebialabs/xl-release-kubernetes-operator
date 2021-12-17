depl = None
try:
    depl = deployment.prepareInitial(yakPackage10.id, multiServerEnv.id)
    depl = deployment.prepareAutoDeployeds(depl)
    depl.deployedApplication.values['orchestrator'] = 'sequential-by-container'

    previewBlock = deployment.taskPreviewBlock(depl).blocks.get(0).block

    assertEquals(2, len(previewBlock.blocks))
    block1Id = previewBlock.blocks[0].id
    block2Id = previewBlock.blocks[1].id

    assertEquals(1, len(previewBlock.blocks[0].steps))
    assertEquals(1, len(previewBlock.blocks[1].steps))

    expectedPreview = "10 GOTO 20\n20 PRINTLN \"Hello World\"\n30 PRINTLN \"I'm a stupid Basic Script\""

    previewStep1 = deployment.taskPreviewBlock(depl, block1Id, 1)
    assertEquals(expectedPreview, previewStep1.metadata["contents"])

    previewStep2 = deployment.taskPreviewBlock(depl, block2Id, 1)
    assertEquals(expectedPreview, previewStep2.metadata["contents"])

    # Check user without task preview
    switchUser('user-without-task-preview')
    previewStep1 = deployment.taskPreviewBlock(depl, block1Id, 1)
    assertFalse('contents' in previewStep1.metadata)

    previewStep2 = deployment.taskPreviewBlock(depl, block2Id, 1)
    assertFalse('contents' in previewStep2.metadata)

finally:
    # the validate should trigger a cache invalidate to get rid of the workdir
    # TODO add webservice to cleanup explicitly
    if depl:
        deployment.validate(depl)
