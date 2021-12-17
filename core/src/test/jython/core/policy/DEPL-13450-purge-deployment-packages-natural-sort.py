## PACKAGES
def deploy(package, env):
    depl = deployment.prepareInitial(package.id, env.id)
    taskId = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(taskId)

devServer = repository.create(factory.configurationItem('Infrastructure/policy-dev-server', 'yak.YakServer', {}))
devEnv = repository.create(factory.configurationItem('Environments/policy-dev-env', 'udm.Environment', {'members': [devServer.id]}))

testServer = repository.create(factory.configurationItem('Infrastructure/policy-test-server', 'yak.YakServer', {}))
testEnv = repository.create(factory.configurationItem('Environments/policy-test-env', 'udm.Environment', {'members': [testServer.id]}))

app3 = repository.create(factory.configurationItem('Applications/policy-app-3', 'udm.Application'))

package1_0 =   repository.create(factory.configurationItem('Applications/policy-app-3/1.0', 'udm.DeploymentPackage'))
package2_0 =   repository.create(factory.configurationItem('Applications/policy-app-3/2.0', 'udm.DeploymentPackage'))
package3_0 =   repository.create(factory.configurationItem('Applications/policy-app-3/3.0', 'udm.DeploymentPackage'))
package4_0 =   repository.create(factory.configurationItem('Applications/policy-app-3/4.0', 'udm.DeploymentPackage'))
package5_0 =   repository.create(factory.configurationItem('Applications/policy-app-3/5.0', 'udm.DeploymentPackage'))
package10_0 =  repository.create(factory.configurationItem('Applications/policy-app-3/10.0', 'udm.DeploymentPackage'))
package100_0 = repository.create(factory.configurationItem('Applications/policy-app-3/100.0', 'udm.DeploymentPackage'))

app3Policy = repository.create(factory.configurationItem('Configuration/policy-app3-policy', 'policy.PackageRetentionPolicy', {'enabled': 'false', 'packageRetention': '4', 'pattern': '^Applications/policy-app-3/.*$'}))

try:
    deployit.executeControlTask('executeJob', app3Policy)

    assertFalse(repository.exists(package1_0.id), package1_0.id)
    assertFalse(repository.exists(package2_0.id), package2_0.id)
    assertFalse(repository.exists(package3_0.id), package3_0.id)
    assertTrue(repository.exists(package4_0.id), package4_0.id)
    assertTrue(repository.exists(package5_0.id), package5_0.id)
    assertTrue(repository.exists(package10_0.id), package10_0.id)
    assertTrue(repository.exists(package100_0.id), package100_0.id)

finally:
    repository.delete(devEnv.id)
    repository.delete(devServer.id)
    repository.delete(testEnv.id)
    repository.delete(testServer.id)
    repository.delete(app3Policy.id)
    repository.delete(app3.id)