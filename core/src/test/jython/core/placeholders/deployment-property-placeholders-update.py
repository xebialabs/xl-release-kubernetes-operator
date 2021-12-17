dict1 = create_random_dict({'entries': {'AGE': 'yak'}})
server1 = create_random_yak_server()
env1 = create_random_environment("placeholders-update", [server1.id], [dict1.id])
package = repository.read("Applications/PlaceholderApp2/2.0")

depl, task = deploy(package, env1)

deployit.startTaskAndWait(task)

updatedPackage = repository.read("Applications/PlaceholderApp2/3.0")

print "Clearing dictionary Entries...."
dict1.entries.clear()

repository.update(dict1)

udepl = deployment.prepareUpgrade(updatedPackage.id, depl.deployedApplication.id)

validations = map(lambda d: d.validations, udepl.deployeds)

flattenedMessages = reduce(lambda v1, v2: v1 + v2, validations)

assertEquals(1, len(flattenedMessages))

assertEquals("Could not resolve the property value(s) \"{{AGE}}\" using the dictionary",
             flattenedMessages[0].getMessage())
