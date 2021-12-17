bp = create_blueprint("Blueprint_For_PlaceHolders")
pck = create_provisioning_package(blueprint_id=bp.id, name="1.0")
provider = create_dummy_provider(name="provider")

template = create_template(package_id=pck.id, name="LocalHost2", type="template.overthere.LocalHost",
                           params={"os": "{{OS}}"})
provisionable = create_dummy_provisionable(package_id=pck.id, name="dummy1",
                                           params={'cardinality': "{{CARDINALITY}}"}, templates=[template])
provisioning_environment = create_provisioning_environment(name="provisioning_environment", providers=[provider])

dic = repository.create(
    factory.configurationItem("Environments/dict", "udm.Dictionary", {'entries': {'OS': "UNIX", 'CARDINALITY': "1"}}))
