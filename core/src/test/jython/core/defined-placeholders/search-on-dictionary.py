from java.util import UUID

dictSalt = UUID.randomUUID().toString()
targetKey = 'target' + dictSalt

# Prepare dictionary
dict1 = repository.create(factory.configurationItem(
    'Environments/%sDictionary1' % dictSalt,
    'udm.Dictionary',
    {'entries':{targetKey:'12345'}}
))

dict2 = repository.create(factory.configurationItem(
    'Environments/%sDictionary2' % dictSalt,
    'udm.Dictionary',
    {'entries':{targetKey:'value'}}
))

# Prepare environment
env = create_random_environment("search-on-dictionary-env", [], [dict1.id, dict2.id])

# Request dictionary list for key
dictValues = placeholder.definedDictionaryPlaceholders(targetKey, "", "")

assertEquals(2, dictValues.size())
assertEquals('12345', dictValues[0].value)
assertEquals(dict1.id, dictValues[0].dictionary.id)
assertEquals(False, dictValues[0].encrypted)

assertEquals('value', dictValues[1].value)
assertEquals(dict2.id, dictValues[1].dictionary.id)
assertEquals(False, dictValues[1].encrypted)

# Request dictionary list for key and value
dictValues = placeholder.definedDictionaryPlaceholders(targetKey, "12", "")

assertEquals(1, dictValues.size())
assertEquals('12345', dictValues[0].value)
assertEquals(dict1.id, dictValues[0].dictionary.id)
assertEquals(False, dictValues[0].encrypted)

# Request dictionary list for key and name
dictValues = placeholder.definedDictionaryPlaceholders(targetKey, "", "Dictionary2")

assertEquals(1, dictValues.size())
assertEquals('value', dictValues[0].value)
assertEquals(dict2.id, dictValues[0].dictionary.id)
assertEquals(False, dictValues[0].encrypted)

# Delete environment and dictionaries
repository.delete(env.id)
repository.delete(dict1.id)
repository.delete(dict2.id)
