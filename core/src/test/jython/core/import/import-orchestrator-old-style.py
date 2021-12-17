importPackage('ImportApp2/8.0')

assertTrue(repository.exists('Applications/ImportApp2/8.0'))

ci = repository.read('Applications/ImportApp2/8.0')
assertEquals(1, ci.orchestrator.size())
assertEquals('container-by-container', ci.orchestrator.get(0))
