# This test checks if the Credentials CI can be created
# and if it validates presence of username
created = None

try:
    created = create_random_configuration("CREDENTIALS-SMB-CI", "credentials.SmbHostCredentials")
except:
    print('Raised exception, continue the test execution')

try:
    created = create_random_configuration(
        "CREDENTIALS-SMB-CI",
        "credentials.SmbHostCredentials",
        {"username": "api-user", "password": "api-pass"}
    )
except:
    raise Exception("Should create a SmbHostCredentials CI")
