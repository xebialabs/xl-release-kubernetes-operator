cis = repository.create([
    factory.configurationItem('Applications/MyApps/MyApplication', 'udm.Application'),
    factory.configurationItem('Applications/MyApps', 'core.Directory')
])
assertEquals(2, len(cis))
assertEquals(0, len(cis[0].validations))
assertEquals(0, len(cis[1].validations))

repository.deleteList(['Applications/MyApps/MyApplication', 'Applications/MyApps'])