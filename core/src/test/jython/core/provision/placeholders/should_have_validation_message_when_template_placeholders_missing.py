from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

provision = deployment.prepareInitial(pck.id, provisioning_environment.id)

try:
    provision1 = deployment.prepareAutoDeployeds(provision)
except DeployitClientException, err:
    exceptionMessage = err.getMessage()
    print exceptionMessage
    assertTrue(exceptionMessage.find("Couldn't resolve cardinality property from [dummy1]") > -1, "Could not replace dictionary keys in {{CARDINALITY}}")
else:
    raise Exception("Should raise exception when cardinality property cannot be resolved")
