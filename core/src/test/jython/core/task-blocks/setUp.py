
def get_task_ids(tasks):
    ret = []
    for t in tasks:
        ret.append(t.id)
    return ret

yakServer = repository.create(factory.configurationItem("Infrastructure/task-blocks-yak1", "yak.YakServer", {}))
securedDirectory = repository.read("Environments/task-blocks-dir")
yakEnv = repository.create(factory.configurationItem("Environments/task-blocks-dir/task-blocks-env1", "udm.Environment", {"members": [yakServer.id]}))
yakEnv2 = repository.create(factory.configurationItem("Environments/task-blocks-env2", "udm.Environment", {"members": [yakServer.id]}))

dummyServer = repository.create(factory.configurationItem('Infrastructure/task-blocks-DummyJeeServer', 'test-v3.DummyJeeServer',
                                            {'numberOfSteps': '10',
                                             'amountOfKBLogFiles': '2',
                                             'stepDelayTimeInMilliSeconds': '1000',
                                             'hostName': 'localhost',
                                             'deploymentGroup': '2'}))

# Creating the roles
user2 = 'task-blocks-user2'
taskListingUser = 'task-blocks-task-listing-user'
taskListingUser2 = 'task-blocks-task-listing-user2'
taskAssigningUser = 'task-blocks-task-assigning-user'
taskTakeoverUser = 'task-blocks-task-takeover-user'
starterUser = 'task-blocks-starter'
otherUser = 'task-blocks-other_user'
