importPackage('ImportApp2/9.0')

assertTrue(repository.exists('Applications/ImportApp2/9.0'))

ci = repository.read('Applications/ImportApp2/9.0')
assertEquals(2, ci.orchestrator.size())
assertEquals('default', ci.orchestrator.get(0))
assertEquals('container-by-container', ci.orchestrator.get(1))
