# Remove roles
security.removeRole("alfa")
security.removeRole("bravo")
security.removeRole("charlie")

# Remove users
security.deleteUser("alfa")
security.deleteUser("bravo")
security.deleteUser("charlie")

# Remove environment directories
repository.delete(envAlfaDir.id)
repository.delete(envBravoDir.id)
repository.delete(envCharlieDir.id)

# Remove infrastructure
repository.delete(yakServerAlfa.id)
repository.delete(yakServerBravo.id)
repository.delete(yakServerCharlie.id)

# Remove applications
repository.delete(appAlfaDir.id)
repository.delete(appBravoDir.id)
repository.delete(appCharlieDir.id)
