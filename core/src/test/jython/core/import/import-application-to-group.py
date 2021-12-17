
directory = create_random_folder("import-my-apps")

importPackage("ImportApp/1.0")
# Explicitly move to the new location
repository.move("Applications/ImportApp", "%s/ImportApp" % directory.id)
assertNotNone(repository.read("%s/ImportApp/1.0" % directory.id))

# This package should be moved automatically
importPackage("ImportApp/3.0")
assertNotNone(repository.read("%s/ImportApp/3.0" % directory.id))
