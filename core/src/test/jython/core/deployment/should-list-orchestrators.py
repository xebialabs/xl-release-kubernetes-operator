orchestrators = proxies.referenceData.listOrchestrators()

# should list orchestrators
message = "should list orchestrator"
assertTrue(orchestrators.contains('sequential-by-container'), message)
assertTrue(orchestrators.contains('sequential-by-composite-package'), message)
assertTrue(orchestrators.contains('parallel-by-container'), message)
assertTrue(orchestrators.contains('parallel-by-composite-package'), message)

# should not expose default orchestrator
message = "should not list default orchestrator"
assertFalse(orchestrators.contains('default'), message)
assertFalse(orchestrators.contains('DefaultOrchestrator'), message)
