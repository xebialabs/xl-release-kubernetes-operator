try:
    repository.copy('Applications','Applications/repo-apps')
except:
    print 'ok'
else:
    raise Exception('Should not be able to copy root node')
