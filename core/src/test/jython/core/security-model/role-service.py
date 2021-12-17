EDIT_PERMISSION = 'security#edit'

def setupNewUser():
    security.createUser('security-model-new-user', DEFAULT_PASSWORD)
    roleService = proxies.roleService
    roleService.create('security-model-new-user')
    security.assignRole('security-model-new-user', ['security-model-new-user'])
    security.grant('login', 'security-model-new-user')
    u = security.readUser('security-model-new-user')
    assertFalse(u.isAdmin(), 'security-model-new-user must not be admin!')

def shouldFailWhenInvokedWithoutPermission(permission, func):
    switchUser('security-model-new-user')
    roleService = proxies.roleService
    assertFalse(security.hasPermission(permission, "global"), "User should not have permission %s" %(permission))
    retval = None
    try:
        retval = func(roleService = roleService)
    except:
        pass
    else:
        raise Exception("Should fail when invoked without permission %s" %(permission))
    return retval

def shouldSucceedWithoutPermission(permission, func):
    switchUser('security-model-new-user')
    roleService = proxies.roleService
    if security.hasPermission(permission, "global") == True:
        raise Exception("User should not have permission %s" %(permission))
    retval = None
    try:
        retval = func(roleService = roleService)
    except:
        raise Exception("Should succeed without permission %s"%(permission))
    return retval

def shouldSucceedWithPermission(permission, func):
    switchUser('admin')
    roleService = proxies.roleService
    retval = func(roleService = roleService)
    return retval

def list():
    availableRoles = shouldSucceedWithoutPermission(EDIT_PERMISSION, lambda roleService: roleService.list())
    if not availableRoles:
        raise Exception("RoleService#list should return some available roles")
    if len(availableRoles) == 0:
        raise Exception("There must be some roles")

def listMyRoles():
    def prepare(roleService):
        roleService.create('security-model-test-role')
        roleService.assign('security-model-test-role', 'security-model-new-user')
    shouldSucceedWithPermission(EDIT_PERMISSION, prepare )
    myRoles = shouldSucceedWithoutPermission(EDIT_PERMISSION, lambda roleService: roleService.listMyRoles())

    if 'security-model-test-role' not in myRoles:
        raise Exception("User 'security-model-new-user' should have role 'security-model-test-role' in %s"%(myRoles))

def listRoles():
    role = 'security-model-dummyRole'
    def prepare(roleService):
        roleService.create(role)
        roleService.assign(role, 'admin')
    shouldSucceedWithPermission(EDIT_PERMISSION, prepare)
    shouldFailWhenInvokedWithoutPermission(EDIT_PERMISSION, lambda roleService: roleService.listRoles("admin"))
    adminRoles = shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.listRoles("admin"))
    if role not in adminRoles:
        raise Exception('Admin roles should contain security-model-dummyRole')
    shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.delete('security-model-dummyRole'))

def createRole(role="security-model-new-role"):
    def prepare(roleService):
        roles = roleService.list()
        if role in roles:
            raise Exception("Role '%s' already exists. Cleanup tests!" %(role))
        roleService.create(role)
    shouldSucceedWithoutPermission(EDIT_PERMISSION, lambda roleService: prepare)
    shouldFailWhenInvokedWithoutPermission(EDIT_PERMISSION, lambda roleService: roleService.create(role))
    shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.create(role))
    shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.delete(role))

def assignRole(role="security-model-new-role", principal="admin"):
    shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.create(role))
    shouldFailWhenInvokedWithoutPermission(EDIT_PERMISSION, lambda roleService: roleService.assign(role, principal))
    shouldSucceedWithPermission(EDIT_PERMISSION, lambda  roleService: roleService.assign(role, principal))
    def verify(roleService):
        userRoles = roleService.listRoles(principal)
        if role not in userRoles:
            raise Exception("User %s should have role %s assigned"% (principal, role))
        roleService.delete(role)
    shouldSucceedWithPermission(EDIT_PERMISSION, verify)

def unassignRole(role="security-model-new-role-should-be-missing", principal="admin"):
    def prepare(roleService):
        roleService.create(role)
        roleService.assign(role, principal)
        userRoles = roleService.listRoles(principal)
        if role not in userRoles:
            raise Exception("User %s should have role %s assigned"% (principal, role))
    shouldSucceedWithPermission(EDIT_PERMISSION, prepare)
    shouldFailWhenInvokedWithoutPermission(EDIT_PERMISSION, lambda roleService: roleService.unassign(role, principal))
    shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.unassign(role, principal))
    userRoles = shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.listRoles(principal))
    if role in userRoles:
        raise Exception("User %s should not have role %s assigned"%(principal,role))

def rename():
    def prepare(roleService):
        roleService.create("security-model-original-name")
        roleService.assign("security-model-original-name", "security-model-new-user")
        roles = roleService.listRoles('security-model-new-user')
        if "security-model-original-name" not in roles:
            raise Exception("security-model-original-name not added as role to security-model-new-user")
    shouldSucceedWithPermission(EDIT_PERMISSION, prepare)
    shouldFailWhenInvokedWithoutPermission(EDIT_PERMISSION, lambda roleService: roleService.rename("security-model-original-name", "security-model-new-name"))
    shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.rename("security-model-original-name", "security-model-new-name"))

    def verify(roleService):
        roles = roleService.listRoles('security-model-new-user')
        if "security-model-original-name" in roles:
            raise Exception("security-model-original-name should not be a role of security-model-new-user")
        if "security-model-new-name" not in roles:
            raise Exception("security-model-new-name should be a role of security-model-new-user")
    shouldSucceedWithPermission(EDIT_PERMISSION, verify)

def delete():
    def prepare(roleService):
        roleService.create("security-model-original-name")
        roleService.assign("security-model-original-name", "security-model-new-user")
        roles = roleService.listRoles('security-model-new-user')
        if "security-model-original-name" not in roles:
            raise Exception("security-model-original-name not added as role to security-model-new-user")
    shouldSucceedWithPermission(EDIT_PERMISSION, prepare)
    shouldFailWhenInvokedWithoutPermission(EDIT_PERMISSION, lambda roleService: roleService.delete("security-model-original-name"))
    shouldSucceedWithPermission(EDIT_PERMISSION, lambda roleService: roleService.delete("security-model-original-name"))

    def verify(roleService):
        roles = roleService.listRoles('security-model-new-user')
        if "security-model-original-name" in roles:
            raise Exception("security-model-original-name should not be a role of security-model-new-user")
    shouldSucceedWithPermission(EDIT_PERMISSION, verify)

# test rest api calls on role service
setupNewUser()
list()
listRoles()
listMyRoles()
createRole()
assignRole()
unassignRole()
rename()
delete()

security.deleteUser('security-model-new-user')
security.removeRole('security-model-new-user')
security.removeRole('security-model-new-role-should-be-missing')
security.removeRole('security-model-new-name')
security.removeRole('security-model-test-role')
