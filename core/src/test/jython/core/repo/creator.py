app_id = 'Applications/yak-creatorApp'

app = repository.create(factory.configurationItem(app_id, 'udm.Application'))
package = repository.create(factory.configurationItem(app_id + "/1.0", "udm.DeploymentPackage", {'application':app_id}))
ci_id = app_id + '/1.0/yakWithCreator'
deployable = repository.create(factory.configurationItem(ci_id, 'yak.YakWithCreator'))

assert_exists(package.id + '/CreatorCi')
assert_not_exists(ci_id)
repository.delete(app_id)
