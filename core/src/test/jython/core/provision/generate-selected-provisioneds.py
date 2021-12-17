from asserts import assert_equals

provision = deployment.prepareInitial(pck.id, provisioning_environment.id)

print "provision 1"
print provision.id

selectedProvisionableIds = [pr_able.id]

provision = deployment.generateSelectedDeployeds(selectedProvisionableIds, provision)
print "provision after selected provisioneds"
print provision.id
print provision.deployeds

assert_equals(1, len(provision.deployeds), "One provisioned should be created for selected provisionable.")
