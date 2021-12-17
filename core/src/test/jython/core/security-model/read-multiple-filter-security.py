switchUser('security-model-user')

try:
	repository.read('Applications/security-model-dir')
except:
	print("ok")
else:
	raise Exception("should not read")


read = repository.read(['Applications/security-model-dir'])
assertEquals(0, len(read))
