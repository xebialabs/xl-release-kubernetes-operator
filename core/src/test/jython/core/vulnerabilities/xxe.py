from com.xebialabs.deployit.integration.test.support import TemporaryDirectoryHolder
from com.google.common.io import Files
from com.google.common.base import Charsets

from java.io import File

from org.apache.http.client.methods import HttpPost
from org.apache.http.client import HttpResponseException
from org.apache.http.entity import StringEntity
from org.apache.http.impl.client import BasicResponseHandler
from org.apache.http.impl.client import DefaultHttpClient

import base64
import string

username = "admin"
password = "admin"

file = File(TemporaryDirectoryHolder.getTemporaryDirectory(), "vulnerability.xxe")
httpclient = DefaultHttpClient()

base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
entity = StringEntity(
    "<!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///" + file.path + "\">]><configuration-item><id>&xxe;</id><configuration-item-type-name>&xxe;</configuration-item-type-name></configuration-item>")
Files.write("I am vulnerable", file, Charsets.UTF_8)

request = HttpPost("http://localhost:%s%s/deployit/repository/ci/Environments/xxe-env" % (_global_integration_test_port, _context_root))
request.addHeader("Content-Type", "application/xml")
request.addHeader("Authorization", "Basic %s" % base64string)
request.setEntity(entity)

responseHandler = BasicResponseHandler()

try:
    httpclient.execute(request, responseHandler)
except HttpResponseException, e:
    exceptionMessage = e.getMessage()
    print exceptionMessage
    assertEquals(500, e.getStatusCode())
    assertFalse(string.find(exceptionMessage, "vulnerable") > -1)
else:
    raise Exception("Should have a 500")

file.delete()
