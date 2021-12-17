from asserts import assert_equals

provision = deployment.prepareInitial(pck5.id, provisioning_environment.id)

print "provision 1"
print provision.id

provision = deployment.generateSelectedDeployeds([pr_able5_1.id], provision)
print "provision after selected provisioneds"
print provision.deployeds

assert_equals(1, len(provision.deployeds), "One provisioned should be created for selected provisionable.")

provision = deployment.generateSelectedDeployeds([pr_able5_2.id], provision)
print "provision after second selected provisioneds"
print provision.deployeds

assert_equals(2, len(provision.deployeds),
              "Two provisioned should be created. One for existing and one for selected provisionable.")