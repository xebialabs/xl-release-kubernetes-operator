import time
from com.xebialabs.deployit.booter.remote.resteasy import DeployitClientException

attempts = 30
expected_number_of_workers = 2
actual_number_of_workers = 0

while(attempts > 0):
  print("Left attempt # %s " % attempts)
  actual_number_of_workers = workers.list().size()
  if expected_number_of_workers != actual_number_of_workers:
    time.sleep(10)
    attempts -= 1
  else:
    break

if (attempts == 0):
    fail("Expected to find %s number of workers, but actually is %s " % (expected_number_of_workers, actual_number_of_workers))
