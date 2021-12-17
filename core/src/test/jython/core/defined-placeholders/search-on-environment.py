suitePrefix = 'search-on-environment-'

# Prepare dictionary
dict1 = create_random_dict({'entries':{'target':'12345'}})
dict2 = create_random_dict({'entries':{'target-two':'value'}})

# Prepare environment
env1 = create_random_environment("%senv1" % suitePrefix, [], [dict1.id, dict2.id])

# Prepare environment
env2 = create_random_environment("%senv2" % suitePrefix, [], [dict1.id])

# Request dictionary list for key
environments = placeholder.definedEnvironmentPlaceholders("target", suitePrefix)

assertEquals(2, environments.size())
assertEquals(env1.id, environments[0].id)
assertEquals(env2.id, environments[1].id)

# Request dictionary list for key
environments = placeholder.definedEnvironmentPlaceholders("target-two", suitePrefix)

assertEquals(1, environments.size())
assertEquals(env1.id, environments[0].id)

# Request dictionary list for key
environments = placeholder.definedEnvironmentPlaceholders("target", "env2")

assertEquals(1, environments.size())
assertEquals(env2.id, environments[0].id)

# Delete environments and dictionaries
repository.delete(env1.id)
repository.delete(env2.id)
repository.delete(dict1.id)
repository.delete(dict2.id)
