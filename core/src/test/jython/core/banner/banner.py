from ai.digital.deploy.sql.model import BannerInfo
from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

otherUser = 'otherUser'
security.createUser(otherUser, DEFAULT_PASSWORD)
security.assignRole(otherUser, [otherUser])
security.grant('login', otherUser)

banner = proxies.banner

info = banner.getBannerInfo(BannerInfo.BannerKind.MAINTENANCE)
assertEquals(None, info.content)
assertEquals("MAINTENANCE", info.kind.name())

banner.updateBannerInfo(BannerInfo(BannerInfo.BannerKind.MAINTENANCE, "Maintenance mode is on"))
info = banner.getBannerInfo(BannerInfo.BannerKind.MAINTENANCE)
assertEquals("Maintenance mode is on", info.content)
assertEquals("MAINTENANCE", info.kind.name())

switchUser(otherUser)

try:
    banner.updateBannerInfo(BannerInfo(BannerInfo.BannerKind.MAINTENANCE, "Maintenance mode is on"))
except DeployitClientException, ex:
    assertTrue("You do not have admin permission" in ex.message)

switchUser('admin')
security.deleteUser(otherUser)
security.removeRole(otherUser)
