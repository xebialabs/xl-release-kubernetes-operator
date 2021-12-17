#
# Clean op CI's from the repository
#
def deleteServers(serverName, numberOfServers):
    for i in range(0, numberOfServers):
        repository.delete('Infrastructure/' + serverName + str(i))
    return

def deleteHost(serverName):
    repository.delete('Infrastructure/' + "Host-with-" + serverName)
    
def deleteEnvironments(environmentName, environmentSize):
    for i in range(0, environmentSize):
        repository.delete('Environments/' + str(i) + environmentName + str(i))
    return

deleteEnvironments("export-hostEnv", 1)
deleteEnvironments("export-exportEnv", 10)
deleteHost("export-hostEnvServer")
deleteServers("export-exportServer", 1)
deleteServers("export-hostEnvServer", 2)
repository.delete('Applications/export-tinyExportApp')
repository.delete('Applications/export-smallExportApp')