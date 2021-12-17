print deployit.listImportablePackages()

importedPackage = importPackage("ImportApp/3.0")
middlewareResource = repository.read("%s/petclinicDS" % importedPackage.id)

if middlewareResource is None:
    raise Exception("Could not find the resource which should have been imported")
