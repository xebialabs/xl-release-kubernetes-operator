# This test checks if the Credentials CI can be attached to the CIFS Host Infrastructure item

credentials_ci = create_random_configuration("CREDENTIALS-CI-FOR-CIFS-HOSTS", "credentials.SmbHostCredentials", {"username": "api-user", "password": "api-pass"})

# attach to existing Host CI
server1 = create_random_host(
    "CREDENTAILS-CIFS-HOST-1",
    "overthere.CifsHost",
    {'accessMethod':'SSH_SFTP','os':'UNIX','address':'myServer', 'username':'foo', 'password':'bar'}
)

server1.credentials = credentials_ci.id
repository.update(server1)

updated_server1 = repository.read(server1.id)
assertTrue(updated_server1.values["credentials"] == credentials_ci.id)

# create new host CI with Credentials as a auth mechanism
server2 = create_random_host(
    "CREDENTAILS-CIFS-HOST-2",
    "overthere.CifsHost",
    {'accessMethod':'SSH_SFTP','os':'UNIX','address':'myServer', 'credentials': credentials_ci.id}
)

updated_server2 = repository.read(server2.id)
assertTrue(updated_server2.values["credentials"] == credentials_ci.id)

repository.delete(server1.id)
repository.delete(server2.id)
