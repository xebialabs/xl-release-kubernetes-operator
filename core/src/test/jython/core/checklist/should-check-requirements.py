
switchUser(deployUsername)
app = deployit.importPackage("ChecklistApp/1.0")
depl = deployment.prepareInitial(app.id, env.id)
depl = deployment.prepareAutoDeployeds(depl)

try:
    taskId = deployment.createDeployTask(depl).id
except:
    pass
else:
    raise Exception("Should not be allowed to deploy application")

switchUser('admin')

# cleanup
repository.delete("Applications/ChecklistApp")