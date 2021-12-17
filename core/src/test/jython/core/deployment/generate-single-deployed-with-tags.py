# Import package with tags
yakTagPackage = repository.read('Applications/DeploymentApp/1.0-with-tags')

# Create env with tags
yakServerTag1 = create_random_yak_server("deployment-wrongTag", { "tags": ['wrongTag']})
yakTagEnv = create_random_environment("env1", [yakServerTag1.id])

depl = deployment.prepareInitial(yakTagPackage.id, yakTagEnv.id)
depl = deployment.generateSingleDeployed(yakTagPackage.id + '/tag1.yak', yakServerTag1.id, None, depl)
assertNotNone(depl.deployeds)

# Deployeds should be (1):
# - tag1.yak -> wrongTag1
assertEquals(1, len(depl.deployeds))

def f(deployed): return deployed.id == '%s/tag1.yak' % yakServerTag1.id
assertEquals(1, len(filter(f, depl.deployeds)))
