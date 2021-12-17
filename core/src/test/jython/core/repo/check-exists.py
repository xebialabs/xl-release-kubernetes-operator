id = "Infrastructure/repo-codeFoodBar"
assertFalse(repository.exists(id))
repository.create(factory.configurationItem(id, "yak.YakServer", {}))
assertTrue(repository.exists(id))
repository.delete(id)
assertFalse(repository.exists(id))
