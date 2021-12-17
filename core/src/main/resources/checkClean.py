switchUser('admin')

proxyRepo = proxies.getRepository()

# Finding left over CIs
entityIds = repository.search(None)
entityIds.remove('Applications')
entityIds.remove('Environments')
entityIds.remove('Infrastructure')
entityIds.remove('Configuration')
if len(entityIds) > 0:
    ids = ""
    for e in entityIds:
        ids = ids + e + "; "
    raise Exception("Repository was not clean! found: " + ids)

# Finding left over tasks
tasks = task2.allCurrentTaskSummaries
if len(tasks) > 0:
    descriptions = ""
    for t in tasks:
        descriptions = descriptions + t.description + "; "
    raise Exception("Running tasks left! " + descriptions)

# Finding left over roles

roles = security.getRoleNames()
if len(roles) > 0:
    descriptions = ""
    for r in roles:
        descriptions = descriptions + r + "; "
    raise Exception("Roles left! " + descriptions)
