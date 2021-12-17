import urllib2, base64, string
from urllib2 import HTTPError

username = "admin"
password = "admin"

request_url = "http://localhost:%s%s/deployit/repository/query?resultsPerPage=-1&typeName=udm.DeploymentPackage&page=0&parent=Applications/PetClinic-Ear'" % (_global_integration_test_port, _context_root)
print "Connecting to %s" % request_url
request = urllib2.Request(request_url)

base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Content-Type", "application/xml")
request.add_header("Authorization", "Basic %s" % base64string)
try:
	result = urllib2.urlopen(request)
	assertEquals(200, result.code)
except HTTPError, e:
	raise Exception("Should not fail because of single quote(')", request)
