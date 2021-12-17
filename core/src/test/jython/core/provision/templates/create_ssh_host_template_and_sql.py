
ssh_host = create_template(package_id=provision_package.id, name="SshHost", type="template.overthere.SshHost",
                params={"os": "UNIX", "username": "vagrant", "address": "localhost"})

sql = create_template(package_id=provision_package.id, name="Sql", type="template.sql.MySqlClient", params={"mySqlHome": "/opt", "databaseName": "DB"})
assert_exists(ssh_host.id)
assert_exists(sql.id)
delete([ssh_host, sql])
