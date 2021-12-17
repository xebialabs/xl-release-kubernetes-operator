# Import package with tags
yakTagPackage = repository.read('Applications/DeploymentApp/1.0-with-tags')

# Create env with tags
yakServerTag1 = create_random_yak_server("deployment-yakTag1", { "tags": ['tag1']})
yakServerTag2 = create_random_yak_server("deployment-yakTag2", { "tags": ['tag2']})
yakTagEnv = create_random_environment("env1", [yakServerTag1.id, yakServerTag2.id])

depl = deployment.prepareInitial(yakTagPackage.id, yakTagEnv.id)
depl = deployment.prepareAutoDeployeds(depl)
assertNotNone(depl.deployeds)

# Deployeds should be (4):
# - tag1.yak -> yakTag1
# - tag2.yak -> yakTag2
# - tag1and2.yak -> yakTag1
# - tag1and2.yak -> yakTag2
assertEquals(4, len(depl.deployeds))

def f(deployed): return deployed.id == '%s/tag1.yak' % yakServerTag1.id
assertEquals(1, len(filter(f, depl.deployeds)))

def f(deployed): return deployed.id == '%s/tag2.yak' % yakServerTag2.id
assertEquals(1, len(filter(f, depl.deployeds)))

def f(deployed): return deployed.id == '%s/tag1and2.yak' % yakServerTag1.id
assertEquals(1, len(filter(f, depl.deployeds)))

def f(deployed): return deployed.id == '%s/tag1and2.yak' % yakServerTag2.id
assertEquals(1, len(filter(f, depl.deployeds)))
