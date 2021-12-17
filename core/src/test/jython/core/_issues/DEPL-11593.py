cis = repository.create([
    factory.configurationItem('Applications/MyApplication-11593', 'udm.Application'),
    factory.configurationItem('Applications/MyApplication-11593/1.0', 'udm.DeploymentPackage'),
    factory.configurationItem('Applications/MyApplication-11593/1.0/archive001', 'file.Archive', {'fileUri': "http://localhost:%s%s/deployit/internal/configuration/license-info" % (_global_integration_test_port, _context_root)})
])
assertEquals(3, len(cis))
assertEquals(0, len(cis[0].validations))
assertEquals(0, len(cis[1].validations))
assertEquals(0, len(cis[2].validations))

repository.delete('Applications/MyApplication-11593/1.0/archive001')
repository.delete('Applications/MyApplication-11593/1.0')
repository.delete('Applications/MyApplication-11593')