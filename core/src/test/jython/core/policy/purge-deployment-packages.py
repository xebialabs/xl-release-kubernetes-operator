## PACKAGES
def deploy(package, env):
    depl = deployment.prepareInitial(package.id, env.id)
    taskId = deployment.createDeployTask(depl).id
    deployit.startTaskAndWait(taskId)

devServer = repository.create(factory.configurationItem('Infrastructure/policy-dev-server', 'yak.YakServer', {}))
devEnv = repository.create(factory.configurationItem('Environments/policy-dev-env', 'udm.Environment', {'members': [devServer.id]}))

testServer = repository.create(factory.configurationItem('Infrastructure/policy-test-server', 'yak.YakServer', {}))
testEnv = repository.create(factory.configurationItem('Environments/policy-test-env', 'udm.Environment', {'members': [testServer.id]}))

app1 = repository.create(factory.configurationItem('Applications/policy-app-1', 'udm.Application'))
app2 = repository.create(factory.configurationItem('Applications/policy-app-2', 'udm.Application'))
app3 = repository.create(factory.configurationItem('Applications/retain-all-app-3', 'udm.Application'))


#
package100 = repository.create(factory.configurationItem('Applications/policy-app-1/1.0.0', 'udm.DeploymentPackage'))
package110 = repository.create(factory.configurationItem('Applications/policy-app-1/1.1.0', 'udm.DeploymentPackage'))
package200 = repository.create(factory.configurationItem('Applications/policy-app-1/2.0.0', 'udm.DeploymentPackage'))
package200s = repository.create(factory.configurationItem('Applications/policy-app-1/2.0.0-SNAPSHOT', 'udm.DeploymentPackage'))
package201s = repository.create(factory.configurationItem('Applications/policy-app-1/2.0.1-SNAPSHOT', 'udm.DeploymentPackage'))
package300 = repository.create(factory.configurationItem('Applications/policy-app-1/3.0.0', 'udm.DeploymentPackage'))
package350 = repository.create(factory.configurationItem('Applications/policy-app-1/3.5.0', 'udm.DeploymentPackage'))

package10s = repository.create(factory.configurationItem('Applications/policy-app-2/1.0-SNAPSHOT', 'udm.DeploymentPackage'))
package20s = repository.create(factory.configurationItem('Applications/policy-app-2/2.0-SNAPSHOT', 'udm.DeploymentPackage'))

package10 = repository.create(factory.configurationItem('Applications/retain-all-app-3/1.0', 'udm.DeploymentPackage'))
package11 = repository.create(factory.configurationItem('Applications/retain-all-app-3/1.1', 'udm.DeploymentPackage'))
package20 = repository.create(factory.configurationItem('Applications/retain-all-app-3/2.0', 'udm.DeploymentPackage'))

deploy(package110, testEnv)
deploy(package201s, devEnv)
deploy(package10s, devEnv)
deploy(package11, devEnv)


appReleasePolicy = repository.create(factory.configurationItem('Configuration/policy-app-release-policy', 'policy.PackageRetentionPolicy', {'enabled': 'false', 'packageRetention': '2', 'pattern': '^Applications/policy.*/\d{1,8}(?:\.\d{1,6})?(?:\.\d{1,6})?(?:-\d+)?$'}))
app1SnapshotPolicy = repository.create(factory.configurationItem('Configuration/policy-app1-snapshot-policy', 'policy.PackageRetentionPolicy', {'enabled': 'false', 'packageRetention': '5', 'pattern': '^Applications/policy-app-1/\d{1,8}(?:\.\d{1,6})?(?:\.\d{1,6})?(?:-\d+)?-SNAPSHOT$$'}))
app2Policy = repository.create(factory.configurationItem('Configuration/policy-app2-policy', 'policy.PackageRetentionPolicy', {'enabled': 'false', 'packageRetention': '0', 'pattern': '^Applications/policy-app-2/.*$'}))
app3Policy = repository.create(factory.configurationItem('Configuration/retain-all-app3-policy', 'policy.PackageRetentionPolicy', {'enabled': 'false', 'packageRetention': '0', 'packageDaysRetention': '5', 'pattern': '^Applications/retain-all-app-3/.*$'}))

try:
    deployit.executeControlTask('executeJob', appReleasePolicy)
    deployit.executeControlTask('executeJob', app1SnapshotPolicy)
    deployit.executeControlTask('executeJob', app2Policy)
    deployit.executeControlTask('executeJob', app3Policy)

    assertFalse(repository.exists(package100.id), package100.id)
    assertTrue(repository.exists(package110.id), package110.id)
    assertFalse(repository.exists(package200.id), package200.id)
    assertTrue(repository.exists(package200s.id), package200s.id)
    assertTrue(repository.exists(package201s.id), package201s.id)
    assertTrue(repository.exists(package300.id), package300.id)
    assertTrue(repository.exists(package350.id), package350.id)

    assertTrue(repository.exists(package10s.id), package10s.id)
    assertFalse(repository.exists(package20s.id), package20s.id)

    assertTrue(repository.exists(package10.id), package10.id)
    assertTrue(repository.exists(package11.id), package11.id)
    assertTrue(repository.exists(package20.id), package20.id)


finally:
    repository.delete(appReleasePolicy.id)
    repository.delete(app1SnapshotPolicy.id)
    repository.delete(app2Policy.id)
    repository.delete(app3Policy.id)
    repository.delete(devEnv.id)
    repository.delete(devServer.id)
    repository.delete(testEnv.id)
    repository.delete(testServer.id)
    repository.delete(app1.id)
    repository.delete(app2.id)
    repository.delete(app3.id)

