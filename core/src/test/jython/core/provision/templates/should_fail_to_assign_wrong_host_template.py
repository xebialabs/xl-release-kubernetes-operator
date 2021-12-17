
ssh_host = create_template(package_id=provision_package_2.id, name="SshHost", type="template.overthere.SshHost",
                params={"os": "UNIX", "username": "vagrant", "address": "localhost"})

sql = create_template(package_id=provision_package_2.id, name="Sql", type="template.sql.MySqlClient", params={"mySqlHome": "/opt", "databaseName": "DB"})

manifest = create_dummy_manifest(provisionable_id=provisionable_2_1.id, name="tomcat.pp", host_template=sql, content="Some not real content")
print str(manifest)
assert_true("must extend type template.overthere.Host" in str(manifest), "Exception error does not indicated that host template validator failed")
