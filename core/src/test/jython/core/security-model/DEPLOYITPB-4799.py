username = 'issues-user-one'
password = 'Pa$$w*rd1'

security.createUser(username, password)
security.assignRole(username, [username])
security.grant("login", username)

security.logout()
security.login(username, password)

security.logout()
security.login('admin', 'admin')

security.revoke("login", username)
security.deleteUser(username)
security.removeRole(username)
