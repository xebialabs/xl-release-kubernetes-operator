from java.util import Collections
from utils import get_file_in_folder
from utils import get_tmp_folder

blueprint = create_blueprint("BlueprintForExport")
provisioning_package = create_provisioning_package(blueprint_id=blueprint.id, name="1.0")
ssh_host = create_template(package_id=provisioning_package.id, name="SshHost", type="template.overthere.SshHost",
                           params={"os": "UNIX", "username": "vagrant", "address": "localhost"})
sql = create_template(package_id=ssh_host.id, name="MySqlClient", type="template.sql.MySqlClient",
                      params={"mySqlHome": "/opt", "databaseName": "DB"})
dictionary = create_template(package_id=provisioning_package.id, name="Dictionary", type="template.udm.Dictionary",
                             params={"entries": {"KEY": "VALUE"}})
provisioning_package.templates = Collections.singleton(dictionary.id)
update(provisioning_package)
provisionable = create_dummy_provisionable(package_id=provisioning_package.id, name="dummy1",
                                           params={'cardinality': "{{CARDINALITY}}"}, templates=[ssh_host])
manifest = create_dummy_manifest(provisionable_id=provisionable.id, name="tomcat.pp", host_template=ssh_host, content="Some not real content")
module = create_dummy_module(manifest_id=manifest.id, name="tomcat-module")

tmp_folder = get_tmp_folder("provision_export_import")
repository.exportDar(tmp_folder, provisioning_package.id)
print tmp_folder

delete([blueprint])

deployit.importPackage(get_file_in_folder(tmp_folder, blueprint.name + "-" + provisioning_package.name + ".dar"))
assert_exists(blueprint.id)
assert_exists(provisioning_package.id)
assert_exists(ssh_host.id)
assert_exists(sql.id)
assert_exists(dictionary.id)
assert_exists(provisionable.id)
assert_exists(manifest.id)
assert_exists(module.id)

delete([blueprint])