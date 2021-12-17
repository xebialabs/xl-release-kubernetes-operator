
def assertPermissions(p):
    assertEquals(1, p.size())
    assertEquals(1, p.get("global").size())
    assertEquals("login", p.get("global").iterator().next())

switchUser('security-model-user')

assertPermissions(security.getPermissions())
assertPermissions(security.getPermissions("security-model-user"))
