darFile = "src/test/resources/packages/import/test-package-remote-artifact.dar"
importPackage = importPackage(darFile)

#read the imported package from repository
assertNotNone(importPackage)
