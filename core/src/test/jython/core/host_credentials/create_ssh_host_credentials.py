# This test checks if the Credentials CI can be created
# and if it validates presence of username
created = None

try:
    credentials = create_random_configuration("CREDENTIALS-SSH-CI", "credentials.SshHostCredentials")
except:
    print('Raised exception, continue the test execution')

credentials.password = "api-pass"
credentials.username = "api-user"

try:
    created = repository.create(credentials)
except:
    raise Exception("Should create a SshHostCredentials CI")
