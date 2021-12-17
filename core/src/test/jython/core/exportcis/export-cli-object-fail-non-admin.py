username = 'exportcis-nonAdmin'
try:
    switchUser(username)
    repository.exportCis('Applications')
except:
    pass
else:
    raise Exception("Non-admin users should not be allowed to export CIs")
finally:
    switchUser('admin')
