# this test ensures the authentication of the server extensions api works correctly with different user then admin

import urllib2, base64, string
from urllib2 import HTTPError

username = "issues-user-john"

security.createUser(username, DEFAULT_PASSWORD)
security.assignRole(username, [username])
security.grant('login', username)
security.grant('admin', username)

request = urllib2.Request("http://localhost:%s/api/metadata" % _global_integration_test_port)
base64string = base64.encodestring('%s:%s' % (username, DEFAULT_PASSWORD)).replace('\n', '')
request.add_header("Content-Type", "application/xml")
request.add_header("Authorization", "Basic %s" % base64string)
try:
    result = urllib2.urlopen(request)
    assertEquals(200, result.code)
except HTTPError, e:
    raise Exception("Failed to display extensions listing page")

security.deleteUser(username)
security.revoke('login', username)
security.revoke('admin', username)
security.removeRole(username)
