licenseInfo = proxies.configuration.licenseInfo

assertEquals("XL Deploy", licenseInfo.product)
assertEquals("XebiaLabs - Testing Only!", licenseInfo.licensedTo)
assertEquals("Jython Test", licenseInfo.contact)
assertEquals("2037-01-01", licenseInfo.expiresAfter)
assertEquals(1, licenseInfo.licensedCiUsages.size())
assertEquals("udm.Application", licenseInfo.licensedCiUsages[0].ciType)
assertEquals(10000, licenseInfo.licensedCiUsages[0].licensed)
assertEquals("[tomcat-plugin, was-plugin, iis-plugin]", str(licenseInfo.licensedPlugins))
assertEquals("24x7", licenseInfo.supportPolicy)
assertEquals("2", licenseInfo.maxUsers)
assertEquals("Enterprise", licenseInfo.edition)
