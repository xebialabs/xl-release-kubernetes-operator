darFile = "src/test/resources/packages/import/test-provisioning-package.dar"
importPackage = importPackage(darFile)

#read the imported package from repository
assertNotNone(importPackage)
