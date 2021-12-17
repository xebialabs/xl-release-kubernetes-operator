pkg4 = repository.read('Applications/DeploymentApp/4.0')

env = create_random_environment_with_yak_server("env1")

depl = deployment.prepareInitial(pkg4.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)
assertEquals(2, len(depl.deployeds))

for d in depl.deployeds:
    if d.name == "test.yak":
        depl.deployeds.remove(d)

assertEquals(1, len(depl.deployeds))
