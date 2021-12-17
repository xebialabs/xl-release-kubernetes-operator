import urllib2, base64

def requestUrl(url):
    request = urllib2.Request(url)
    return urllib2.urlopen(request)

security.logout()

# check redirect to keycloak
response1 = requestUrl('http://localhost:4516/oauth2/authorization/xl-deploy?entryPoint=/explorer')
assertTrue(response1.getcode() == 200, str(response1.getcode()))
keycloakLocation = response1.geturl()
assertTrue(
    keycloakLocation.startswith('http://localhost:8080/auth/realms/digitalai-platform/protocol/openid-connect/auth?response_type=code&client_id=deploy&scope=openid'),
    keycloakLocation)
assertTrue(keycloakLocation.find('&redirect_uri=http://localhost:4516/login/external-login') > 0, keycloakLocation)

# check external login functionality
response3 = requestUrl('http://localhost:4516/login/external-login')
assertTrue(response3.getcode() == 200, str(response3.getcode()))
keycloakLocation = response3.geturl()
assertTrue(
    keycloakLocation.startswith('http://localhost:8080/auth/realms/digitalai-platform/protocol/openid-connect/auth?response_type=code&client_id=deploy&scope=openid'),
    keycloakLocation)
assertTrue(keycloakLocation.find('&redirect_uri=http://localhost:4516/login/external-login') > 0, keycloakLocation)
