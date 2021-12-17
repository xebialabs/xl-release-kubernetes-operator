from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.base import Charsets
from com.google.common.io import Files

dict = create_random_dict({"entries": {'foo':'John','bar':'XebiaLabs'}})
server = create_random_yak_server("yak1")
env = create_random_environment("env1", [server.id], [dict.id])

package = importPackage('RollbackApp/3.0')

depl = deployment.prepareInitial(package.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "deployedPlaceholders.yak")
depl.deployeds[0].tempFile = file.path
taskId = deployment.createDeployTask(depl).id

deployit.startTaskAndWait(taskId)

assertTrue(file.exists())
lines = Files.readLines(file, Charsets.UTF_8)

assertEquals("My name is John", lines[0])
assertEquals("I work in XebiaLabs", lines[1])

dict.entries = {'foo':'John', 'bar':'unemployed'}
repository.update(dict)

package2 = importPackage('RollbackApp/1.0-rollback')
depl2 = deployment.prepareUpgrade(package2.id, depl.deployedApplication.id)
depl2.deployeds = []
depl2 = deployment.generateSingleDeployed(package2.deployables[0], server.id, 'yak.DeployedYakCheckpointFile', depl2)
depl2 = deployment.generateSingleDeployed(package2.deployables[1], server.id, 'yak.DeployedYakCheckpointFile', depl2)
assertEquals(2, len(depl2.deployeds))

taskid2 = deployment.createDeployTask(depl2).id
deployit.startTaskAndWait(taskid2)

assertFalse(file.exists())

taskid3 = deployment.createRollbackTask(taskid2).id
deployit.startTaskAndWait(taskid3)
deployit.startTaskAndWait(taskid3)
wait_for_task_state(taskid3, TaskExecutionState.DONE)

assertTrue(file.exists())
lines = Files.readLines(file, Charsets.UTF_8)

# Still holds the old dictionary values
assertEquals("My name is John", lines[0])
assertEquals("I work in XebiaLabs", lines[1])

file.delete()
