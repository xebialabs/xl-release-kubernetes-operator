from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

otherUser = 'otherUser'
admin = 'admin'

security.createUser(otherUser, DEFAULT_PASSWORD)
security.assignRole(otherUser, [otherUser])
security.grant('login', otherUser)

switchUser(admin)
try:
    session.getActiveSessions("")
except DeployitClientException, ex:
    print ex.message

sessions = session.getActiveSessions("")
overview = session.getSessionsOverview()

switchUser(otherUser)

try:
    session.getActiveSessions("")
except DeployitClientException, ex:
    assertTrue("You do not have any of the security#edit, security#view permissions" in ex.message)

switchUser('admin')
security.deleteUser(otherUser)
security.removeRole(otherUser)
