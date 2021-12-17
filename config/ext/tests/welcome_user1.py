context.logOutput("Hello " + user)
context.setAttribute("myattr", user)
print(user)

ci = repositoryService.read("Applications/RulesApp/12.0")
if ci is None:
    raise "Should retrieve CI from repository service"

# deployedResult = deploymentService.isDeployed("Applications/YakApp/12.0", "Environments/StepPlanEnv")
# print "The version of the Application is not defined", deployedResult
# if deployedResult is None:
#     raise "Should return true/False"

packages =  packageService.list()
packages = str(len(packages)) + " packages I have"
print "List of packages" + packages

if packages is None:
    raise "Should retrieve CI from the pacakages"

permissions = permissionService.getMyGrantedPermissions()
print  "My permissions" , permissions

readuser   = userService.read('admin')
print  "Reading the user" , readuser
if readuser is None:
    raise "Should read the user"

roles = roleService.list()
print "List of roles" , roles
if roles is None:
    raise "Should have role assigned"

serverService = serverService.getInfo()
print "Server service info", serverService
if serverService is None:
    raise "Should have service info"

from com.xebialabs.deployit.engine.api.execution import FetchMode

tasks = taskBlockService.getAllCurrentTasks(FetchMode.SUMMARY)
print "The List of CurrentTasks" , tasks
if tasks is None:
    raise "Should have the list of currentTasks"


metadatadescriptors = metadataService.listDescriptors()
print "List of all the known types" , metadatadescriptors
if metadatadescriptors is None:
    raise "Should have the list of known type"


