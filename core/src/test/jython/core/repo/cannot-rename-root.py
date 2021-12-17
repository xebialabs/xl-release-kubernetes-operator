try:
    repository.rename('Applications','repo-foo')
except:
    print 'ok'
else:
    raise Exception('Should not be able to rename root node')