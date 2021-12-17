def deleteCis(key):
    cis = None
    if key in locals():
        cis = locals()[key]
    if cis is None and key in globals():
        cis = globals()[key]
    if cis is not None:
        for ciId in reversed(cis):
            repository.delete(ciId)

deleteCis("dslRandomEnvironmentCis")
deleteCis("dslRandomDictCis")
deleteCis("dslRandomConfigurationCis")
deleteCis("dslRandomInfrastructureCis")
deleteCis("dslRandomHostCis")
deleteCis("dslApplicationCis")
deleteCis("dslImportedPackages")
deleteCis("dslFolderCis")
