from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from java.io import File
from com.google.common.io import Files
from com.google.common.base import Charsets
import urllib2, base64, string
from urllib2 import HTTPError

username = "admin"
password = "admin"
wrongpassword = "wrong"

request_url="http://localhost:%s%s/deployit/server/info" % (_global_integration_test_port, _context_root)
print "Connecting to %s" % request_url

request = urllib2.Request(request_url)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Content-Type", "application/xml")
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

request2 = urllib2.Request("http://localhost:%s%s/deployit/server/info" % (_global_integration_test_port, _context_root))
base64string2 = base64.encodestring('%s:%s' % (username, wrongpassword)).replace('\n', '')
request2.add_header("Content-Type", "application/xml")
request2.add_header("Authorization", "Basic %s" % base64string2)
try:
	result2 = urllib2.urlopen(request2)
except HTTPError, e:
	print e.code
	s = e.read()
	print s
	assertTrue(e.code == 401)
else:
	raise Exception("Should have a 401")

