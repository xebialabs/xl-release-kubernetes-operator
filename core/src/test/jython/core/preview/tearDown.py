security.logout()
security.login('admin', 'admin')

repository.delete(previewApp.id)
repository.delete(envDirectory.id)
repository.delete(srv2.id)
repository.delete(srv1.id)
