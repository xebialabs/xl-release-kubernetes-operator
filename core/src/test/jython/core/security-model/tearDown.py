security.logout()
security.login("admin", "admin")

security.deleteUser("security-model-user")
security.revoke('login', 'security-model-user')
security.removeRole('security-model-user')

repository.delete('Environments/security-model-dir')
repository.delete('Infrastructure/security-model-dir')
repository.delete('Applications/security-model-dir')
