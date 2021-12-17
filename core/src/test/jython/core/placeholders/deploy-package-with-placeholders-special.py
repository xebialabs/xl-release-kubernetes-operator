from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.base import Charsets
from com.google.common.io import Files

env = create_random_environment_with_yak_server()

depl = deployment.prepareInitial("Applications/PlaceholderApp/3.0", env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)
assertEquals(1, len(depl.deployeds))
file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployedPlaceholders2.yak")
depl.deployeds[0].tempFile = file.path
depl.deployeds[0].placeholders['foo'] = '<empty>'
depl.deployeds[0].placeholders['bar'] = '<ignore>'

taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)
wait_for_task_state(taskId, TaskExecutionState.DONE)

assertTrue(file.exists())
lines = Files.readLines(file, Charsets.UTF_8)

assertEquals("My name is ", lines[0])
assertEquals("I work in {{bar}}", lines[1])

file.delete()
