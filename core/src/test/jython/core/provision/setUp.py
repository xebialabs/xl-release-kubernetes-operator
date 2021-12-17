from utils import extract_ids

bp = create_blueprint("Blueprint")
pck = create_provisioning_package(blueprint_id=bp.id, name="1.0")
pr_able = create_dummy_provisionable(package_id=pck.id, name="dummy1", params={'cardinality': "1"})

bp_copy = create_blueprint("Blueprint_copy")
pck_copy = create_provisioning_package(blueprint_id=bp_copy.id, name="1.0")
pr_able_copy = create_dummy_provisionable(package_id=pck_copy.id, name="dummy1", params={'cardinality': "1"})

provider = create_dummy_provider(name="provider")

provisioning_environment = create_provisioning_environment(name="provisioning_environment", providers=[provider])

bp3 = create_blueprint("Blueprint3")
pck3 = create_provisioning_package(blueprint_id=bp3.id, name="3.0")
template3 = create_template(package_id=pck3.id, name="LocalHost", type="template.overthere.LocalHost",
                            params={"os": "UNIX"})
provisionable3 = create_dummy_provisionable(package_id=pck3.id, name="dummy3", params={'cardinality': "1"},
                                            templates=[template3])

bp4 = create_blueprint("Blueprint4")
pck4 = create_provisioning_package(blueprint_id=bp4.id, name="1.0")
template4_1 = create_template(package_id=pck4.id, name="TomcatHost", type="template.overthere.LocalHost",
                              params={"os": "UNIX"})
template4_2 = create_template(package_id=template4_1.id, name="TomcatServer", type="template.dummy-tomcat.TomcatServer")
provisionable4 = create_dummy_provisionable(package_id=pck4.id, name="tomcat", params={'cardinality': "1"},
                                            templates=[template4_1])

pck5 = create_provisioning_package(blueprint_id=bp.id, name="5.0")
pr_able5_1 = create_dummy_provisionable(package_id=pck5.id, name="dummy1", params={'cardinality': "1"})
pr_able5_2 = create_dummy_provisionable(package_id=pck5.id, name="dummy2", params={'cardinality': "1"})


pck_with_dict = create_provisioning_package(blueprint_id=bp.id, name="6.0")
template3 = create_template(package_id=pck_with_dict.id, name="dictionary", type="template.udm.Dictionary")
pck_with_dict.boundTemplates = extract_ids([template3])
update(pck_with_dict)
pr_able_dict = create_dummy_provisionable(package_id=pck_with_dict.id, name="dummy1", params={'cardinality': "1"})