from java.util import Collections

provider = create_dummy_provider(name="provider")
provisioning_environment = create_provisioning_environment(name="provisioning_environment", providers=[provider])
provisioning_environment_dir_path = create_provisioning_environment(name="provisioning_environment_dir_path", providers=[provider],dir_path="provisioning-test/path")

blueprint = create_blueprint("ProvisioningApplication")
provision_package = create_provisioning_package(blueprint_id=blueprint.id, name="1.0")

provision_package_2 = create_provisioning_package(blueprint_id=blueprint.id, name="2.0")
template = create_template(package_id=provision_package_2.id, name="LocalHost", type="template.overthere.LocalHost",
                           instance_name="LocalHost", params={"os": "UNIX"})
template_2 = create_template(package_id=provision_package_2.id, name="LocalHost2", type="template.overthere.LocalHost",
                             params={"os": "UNIX"})
template_3 = create_template(package_id=provision_package_2.id, name="LocalHost3", type="template.overthere.LocalHost",
                             params={"os": "UNIX"})
provisionable_2_1 = create_dummy_provisionable(package_id=provision_package_2.id, name="dummy1",
                                               params={'cardinality': "1"}, templates=[template])
provisionable_2_2 = create_dummy_provisionable(package_id=provision_package_2.id, name="dummy2",
                                               params={'cardinality': "2"}, templates=[template_2])
provision_package_2.boundTemplates = Collections.singleton(template_3.id)
update(provision_package_2)

env_test_dir = create_directory("Environments", "provisioning-test")
env_test_path_dir = create_directory(env_test_dir.id, "path")

infra_test_dir = create_directory("Infrastructure", "provisioning-test")
infra_test_path_dir = create_directory(infra_test_dir.id, "path")
