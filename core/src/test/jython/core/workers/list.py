workersList = None
try:
    workersList = workers.list()
except:
    raise Exception("Should be able to get list of Workers")

assertNotEquals(0, len(workersList))

worker = workersList[0]
if worker.local:
    # in case of local worker
    assertEquals("In-process worker", worker.name)
    assertEquals("akka://task-sys", worker.address)
    assertEquals("CONNECTED", worker.state)
else:
    # in case of external worker (test running with -PexternalWorker=true)
    assertTrue("127.0.0.1" in worker.name)
    assertTrue("akka://task-sys@127.0.0.1" in worker.address)
    assertEquals("CONNECTED", worker.state)
