
def get_task_ids(tasks):
    ret = []
    for t in tasks:
        ret.append(t.id)
    return ret

yakPackage = deployit.importPackage('ScheduleApp/1.0')
yakBlockerPackage = deployit.importPackage('ScheduleApp/1.0-blocker')
yakServer = repository.create(factory.configurationItem("Infrastructure/schedule-yak1", "yak.YakServer", {}))
yakDirectory = repository.create(factory.configurationItem("Environments/schedule-dir", "core.Directory"))
yakEnv = repository.create(factory.configurationItem("Environments/schedule-dir/schedule-env2", "udm.Environment", {"members": [yakServer.id]}))

