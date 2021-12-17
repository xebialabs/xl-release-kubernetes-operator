tmpDir = tempfile.mkdtemp()

taskId = repository.exportCis('Applications/TaskBlockApp/1.0', tmpDir)
assertNotNone(taskId)

exportTargetFile = os.path.join(_integration_server_runtime_directory, task2.get(taskId).metadata['exportedFile'])

assertNotNone(exportTargetFile)
assertTrue(exportTargetFile.startswith(os.path.join(_integration_server_runtime_directory, tmpDir)))

deployit.startTaskAndWait(taskId)

assertTrue(os.path.exists(exportTargetFile))

rmdir(tmpDir)
