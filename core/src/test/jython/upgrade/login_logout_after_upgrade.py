DEFAULT_PASSWORD = "Password_1"
LOGIN_ROLE = 'login-role-only'
USER_LOGIN_ROLE = 'user-with-login-role-only'

try:
    #Create user and grant the user with login permission
    user = security.createUser(USER_LOGIN_ROLE, DEFAULT_PASSWORD)
    security.assignRole(LOGIN_ROLE, [user.username])
    security.grant('login', LOGIN_ROLE)

    #Logout as admin and check login and logout with user
    security.logout()
    security.login(user.username, DEFAULT_PASSWORD)
    security.logout()
finally:
    security.login('admin', 'admin')
    security.deleteUser(user.username)
    security.removeRole(LOGIN_ROLE)
