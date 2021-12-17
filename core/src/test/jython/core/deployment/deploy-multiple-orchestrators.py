from com.xebialabs.deployit.core.util import CiUtils

#    <block id="0" state="PENDING" description="Deploy Composite 1.0 to multiple" parallel="false">
#      <block id="0_1" state="PENDING" description="Deploy package YakApp 1.0" parallel="true">
#        <block id="0_1_1" state="PENDING" description="Deploy on container yak1"/>
#        <block id="0_1_2" state="PENDING" description="Deploy on container yak2"/>
#      </block>
#      <block id="0_2" state="PENDING" description="Deploy on container DummyJeeServer"/>
#   </block>

server1 = create_random_yak_server("yak1")
server2 = create_random_yak_server("yak2")
server3 = create_random_dummy_server()
env = create_random_environment("env1", [server1.id, server2.id, server3.id])

compApp = create_random_application('deployment-Composite')
compApp1_0 = repository.create(factory.configurationItem('%s/1.0' % compApp.id, 'udm.CompositePackage', {"packages":["Applications/DeploymentApp/1.0", "Applications/DeploymentApp4/1.0"]}))

depl = deployment.prepareInitial(compApp1_0.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

depl.deployedApplication.values['orchestrator'] = ['sequential-by-composite-package', 'parallel-by-container']

taskId = deployment.createDeployTask(depl).id
task = task2.get(taskId)

rblock = task.block.blocks.get(0).block

assertEquals(2, len(rblock.blocks))
assertEquals("Deploy %s 1.0 on %s" % (CiUtils.getName(compApp.id), CiUtils.getName(env.id)), rblock.description)
assertFalse(rblock.parallel)

yblock = rblock.blocks.get(0)
assertEquals(2, len(yblock.blocks))
assertEquals("Deploy package DeploymentApp 1.0", yblock.description)
assertTrue(yblock.parallel)

y1block = yblock.blocks.get(0)
assertEquals("Deploy on %s" % CiUtils.getName(server1.id), y1block.description)

y2block = yblock.blocks.get(1)
assertEquals("Deploy on %s" % CiUtils.getName(server2.id), y2block.description)

dblock = rblock.blocks.get(1)
assertEquals("Deploy on %s" % CiUtils.getName(server3.id), dblock.description)

task2.cancel(taskId)
