
def get_task_ids(tasks):
    ret = []
    for t in tasks:
        ret.append(t.id)
    return ret

deploymentUser = 'deployment-user'
taskListingUser = 'deployment-task-listing-user'
taskListingUser2 = 'deployment-task-listing-user2'
taskAssigningUser = 'deployment-task-assigning-user'
