dicts = []

dir = repository.create(factory.configurationItem("Environments/dir", "core.Directory"))
assertTrue(repository.exists(dir.id))

dict_entry = "qwerty" * 1000

for n in range(1, 1001):
    dicts.append(repository.create(factory.configurationItem('Environments/dir/repo-dict-{:1}'.format(n), 'udm.Dictionary',
                                                             {'entries':
                                                                 {
                                                                     'foo': dict_entry,
                                                                     'bar': dict_entry,
                                                                     'buzz': dict_entry,
                                                                     'qwe': dict_entry,
                                                                     'rty': dict_entry}})).id)

env = repository.create(factory.configurationItem('Environments/dir/env_with_dicts', 'udm.Environment', {"dictionaries": dicts}))
assertTrue(repository.exists(env.id))

repository.delete(dir.id)
repository.delete(env.id)
