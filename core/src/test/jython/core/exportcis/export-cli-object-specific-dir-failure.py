from java.lang import RuntimeException

try:
    repository.exportCis('Applications/exportcis-i-do-not-exist', "myDir")
except RuntimeException:
    pass
else:
    fail("Expected not found exception here")