from com.xebialabs.deployit.core.api.resteasy import Date
from java.util import ArrayList

#check as admin
report = proxies.report.getTaskReport(Date("2001-01-01T00:00:00.000UTC"), Date("2002-01-01T00:00:00.000UTC"), None, None, 'none', None, None, None, False, None, ArrayList())
assertNotNone(report)

#user not allowed to see reports
switchUser('security-model-user')

try:
    report = proxies.report.getTaskReport(Date("2001-01-01T00:00:00.000UTC"), Date("2002-01-01T00:00:00.000UTC"), None, None, 'none', None, None, None, False, None, ArrayList())
except:
    pass
else:
    raise Exception("Should not be allowed to get report info")

try:
    users = ArrayList()
    users.add("admin")
    states = ArrayList()
    states.add("DONE")
    states.add("PENDING")
    task_id = "af970bf8-e967-471f-b200-3c4f8386bd0e"
    report = proxies.report.getTaskReport(Date("2001-01-01T00:00:00.000UTC"), Date("2002-01-01T00:00:00.000UTC"), None, None, 'none',
                                          users, states, task_id, False, None, ArrayList())
except:
    pass
else:
    raise Exception("Should not be allowed to get report info")