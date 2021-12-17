from java.lang import RuntimeException
from com.xebialabs.deployit.core.util import CiUtils

shopFrontendApp1 = create_random_application("app-dependencies-ShopFrontend")
shopBackendApp1 = create_random_application("app-dependencies-ShopBackend")
env = create_random_environment_with_yak_server("env1")

shopBackendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopBackendApp1.id, 'udm.DeploymentPackage', {}))
shopFrontendPackage_1_0 = repository.create(factory.configurationItem('%s/1.0' % shopFrontendApp1.id, 'udm.DeploymentPackage', {"applicationDependencies": {shopBackendApp1.name: "1.0"}}))

backendDepl = deployment.prepareInitial(shopBackendPackage_1_0.id, env.id)
backendTaskId = deployment.createDeployTask(backendDepl).id
deployit.startTaskAndWait(backendTaskId)

frontendDepl = deployment.prepareInitial(shopFrontendPackage_1_0.id, env.id)
frontendTaskId = deployment.createDeployTask(frontendDepl).id
deployit.startTaskAndWait(frontendTaskId)

try:
    deployment.createUndeployTask(backendDepl.deployedApplication.id)
except RuntimeException, ex:
    assertTrue("Application &#34;%s&#34; cannot be undeployed, because the deployed application &#34;%s&#34; depends on its current version. It requires a version compatible with &#39;1.0&#39;." % (CiUtils.getName(shopBackendApp1.id), CiUtils.getName(shopFrontendApp1.id)) in ex.message, "The exception message doesn't signal that the frontend depends on the backend, instead it says:" + ex.message)
else:
    fail("A Runtime exception should have been thrown due to broken dependency")
