from asserts import assert_equals
import re

provision = None
try:
    provision = deployment.prepareInitial(pck.id, provisioning_environment.id)
    provision = deployment.prepareAutoDeployeds(provision)

    blocks = deployment.taskPreviewBlock(provision).blocks

    assert_equals(2, len(blocks))

    block_1 = blocks[0]
    block_2 = blocks[1]

    assert_equals("0_1", block_1.id)
    assert_equals("0_2", block_2.id)

    assert_equals(3, len(block_1.block.blocks))
    assert_equals(1, len(block_2.block.steps))
    assert_equals("Register deployeds", block_2.block.steps[0].description)

    preview_step1 = deployment.taskPreviewBlock(provision, block_1.block.blocks[1].id, 1)
    print preview_step1.description
    assert_true(True if re.search(r'Create dummy1 instance on provider', preview_step1.description) else False)

finally:
# the validate should trigger a cache invalidate to get rid of the workdir
    if provision:
        deployment.validate(provision)
