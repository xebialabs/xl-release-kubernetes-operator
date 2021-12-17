template = create_template(package_id=provision_package.id, name="SshHost", type="template.overthere.SshHost",
                           params={"os": "UNIX", "username": "vagrant", "address": "localhost"})
assert_exists(template.id)
delete([template])
