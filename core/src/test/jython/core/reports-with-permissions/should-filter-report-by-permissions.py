from org.joda.time import DateTime, DateTimeZone
from java.util import Locale

now = DateTime.now().withZone(DateTimeZone.UTC)

_begin_date = now.withHourOfDay(0).withMinuteOfHour(0).withSecondOfMinute(0).withMillisOfSecond(0)
_end_date = now.withHourOfDay(23).withMinuteOfHour(59).withSecondOfMinute(59)

_begin = _begin_date.toCalendar(Locale.getDefault())
_end = _end_date.toCalendar(Locale.getDefault())

print("begin")
print(_begin_date)

print("_end")
print(_end_date)

username = "alfa"
deploymentSuccess = makeRequest(username, "deploymentSuccess", _begin, _end)[0]
print("deploymentSuccess")
print(deploymentSuccess)

assertEquals(deploymentSuccess["noOfRollbacks"], "8.33")
assertEquals(deploymentSuccess["noOfFailedDeployments"], "0")
assertEquals(deploymentSuccess["noOfSuccessfulDeployments"], "83.33")
assertEquals(deploymentSuccess["noOfAbortedDeployments"], "8.33")

deploymentTrend = makeRequest(username, "deploymentTrend", _begin, _end)[0]
print("deploymentTrend")
print(deploymentTrend)

assertEquals(deploymentTrend["noOfRollbacks"], "1")
assertEquals(deploymentTrend["noOfFailedDeployments"], "0")
assertEquals(deploymentTrend["noOfSuccessfulDeployments"], "10")
assertEquals(deploymentTrend["noOfAbortedDeployments"], "1")
assertEquals(deploymentTrend["percentageSuccessfulDeployments"], "83.33")

top10SuccessfulDeployments = makeRequest(username, "top10SuccessfulDeployments", _begin, _end)
print("top10SuccessfulDeployments")
print(top10SuccessfulDeployments)

assertEquals(top10SuccessfulDeployments[0]["numOfDeployments"], "5")
assertEquals(top10SuccessfulDeployments[0]["environment"], "Alfa/report-alfa")
assertEquals(top10SuccessfulDeployments[0]["totalDeployments"], "5")
assertEquals(top10SuccessfulDeployments[0]["application"], "DeploymentApp-ForReporting-Alfa")
assertEquals(top10SuccessfulDeployments[0]["percentage"], "100")

assertEquals(top10SuccessfulDeployments[1]["numOfDeployments"], "3")
assertEquals(top10SuccessfulDeployments[1]["environment"], "Charlie/report-charlie")
assertEquals(top10SuccessfulDeployments[1]["totalDeployments"], "3")
assertEquals(top10SuccessfulDeployments[1]["application"], "DeploymentApp-ForReporting-Charlie")
assertEquals(top10SuccessfulDeployments[1]["percentage"], "100")

assertEquals(top10SuccessfulDeployments[2]["numOfDeployments"], "2")
assertEquals(top10SuccessfulDeployments[2]["environment"], "Bravo/report-bravo")
assertEquals(top10SuccessfulDeployments[2]["totalDeployments"], "3")
assertEquals(top10SuccessfulDeployments[2]["application"], "DeploymentApp-ForReporting-Bravo")
assertEquals(top10SuccessfulDeployments[2]["percentage"], "66.67")


username = "bravo"
deploymentSuccess = makeRequest(username, "deploymentSuccess", _begin, _end)[0]
print("deploymentSuccess")
print(deploymentSuccess)

assertEquals(deploymentSuccess["noOfRollbacks"], "0")
assertEquals(deploymentSuccess["noOfFailedDeployments"], "0")
assertEquals(deploymentSuccess["noOfSuccessfulDeployments"], "66.67")
assertEquals(deploymentSuccess["noOfAbortedDeployments"], "33.33")

deploymentTrend = makeRequest(username, "deploymentTrend", _begin, _end)[0]
print("deploymentTrend")
print(deploymentTrend)

print(deploymentTrend)
assertEquals(deploymentTrend["noOfRollbacks"], "0")
assertEquals(deploymentTrend["noOfFailedDeployments"], "0")
assertEquals(deploymentTrend["noOfSuccessfulDeployments"], "2")
assertEquals(deploymentTrend["noOfAbortedDeployments"], "1")
assertEquals(deploymentTrend["percentageSuccessfulDeployments"], "66.67")

top10SuccessfulDeployments = makeRequest(username, "top10SuccessfulDeployments", _begin, _end)
print("top10SuccessfulDeployments")
print(top10SuccessfulDeployments)

assertEquals(top10SuccessfulDeployments[0]["numOfDeployments"], "2")
assertEquals(top10SuccessfulDeployments[0]["environment"], "Bravo/report-bravo")
assertEquals(top10SuccessfulDeployments[0]["totalDeployments"], "3")
assertEquals(top10SuccessfulDeployments[0]["application"], "DeploymentApp-ForReporting-Bravo")
assertEquals(top10SuccessfulDeployments[0]["percentage"], "66.67")
