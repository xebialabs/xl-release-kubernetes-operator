package com.xebialabs.deployit.integration.test;

/**
 * Shortcoming in Gradle, we need a test here that extends the test we want to run from the integration:test
 * because Gradle does not scan jar files for tests to execute. See also GRADLE-863
 * TODO fix when Gradle 1.0 is released.
 */

public class CoreTest {
}

class CoreTestGroup0Deployment extends DeployitIntegrationTest {
    public CoreTestGroup0Deployment() {
        super("core/deployment");
    }
}

class CoreTestGroup0TaskBlocks extends DeployitIntegrationTest {
    public CoreTestGroup0TaskBlocks() {
        super("core/task-blocks");
    }
}

class CoreTestGroup0TaskStatus extends DeployitIntegrationTest {
    public CoreTestGroup0TaskStatus() {
        super("core/task-status");
    }
}

class CoreTestGroup0TaskStepLog extends DeployitIntegrationTest {
    public CoreTestGroup0TaskStepLog() {
        super("core/task-step-log");
    }
}

class CoreTestGroup0Rollback extends DeployitIntegrationTest {
    public CoreTestGroup0Rollback() {
        super("core/rollback");
    }
}


class CoreTestGroup1ApplicationDependencies extends DeployitIntegrationTest {
    public CoreTestGroup1ApplicationDependencies() {
        super("core/application_dependencies");
    }
}

class CoreTestGroup1Provision extends DeployitIntegrationTest {
    public CoreTestGroup1Provision() {
        super("core/provision");
    }
}

class SatelliteTestGroup extends DeployitIntegrationTest {
    public SatelliteTestGroup() {
        super("satellite/task-step-log");
    }
}

class UpgradeTestGroup extends DeployitIntegrationTest {
    public UpgradeTestGroup() {
        super("upgrade");
    }
}

class CoreTestGroup1Discovery extends DeployitIntegrationTest {
    public CoreTestGroup1Discovery() {
        super("core/discovery");
    }
}

class CoreTestGroup1Preview extends DeployitIntegrationTest {
    public CoreTestGroup1Preview() {
        super("core/preview");
    }
}

class CoreTestGroup1Rules extends DeployitIntegrationTest {
    public CoreTestGroup1Rules() {
        super("core/rules");
    }
}

class CoreTestGroup1Staging extends DeployitIntegrationTest {
    public CoreTestGroup1Staging() {
        super("core/staging");
    }
}

class CoreTestGroup1Schedule extends DeployitIntegrationTest {
    public CoreTestGroup1Schedule() {
        super("core/schedule");
    }
}

class CoreTestGroup1Control extends DeployitIntegrationTest {
    public CoreTestGroup1Control() {
        super("core/control");
    }
}

class CoreTestGroup1Session extends DeployitIntegrationTest {
    public CoreTestGroup1Session() {
        super("core/sessions");
    }
}


class CoreTestGroup2Export extends DeployitIntegrationTest {
    public CoreTestGroup2Export() {
        super("core/export");
    }
}

class CoreTestGroup2ExportCis extends DeployitIntegrationTest {
    public CoreTestGroup2ExportCis() {
        super("core/exportcis");
    }
}

class CoreTestGroup2Import extends DeployitIntegrationTest {
    public CoreTestGroup2Import() {
        super("core/import");
    }
}

class CoreTestGroup2Maven extends DeployitIntegrationTest {
    public CoreTestGroup2Maven() {
        super("core/maven");
    }
}

class CoreTestGroup2Artifacts extends DeployitIntegrationTest {
    public CoreTestGroup2Artifacts() {
        super("core/artifacts");
    }
}

class CoreTestGroup2EmbeddedArtifact extends DeployitIntegrationTest {
    public CoreTestGroup2EmbeddedArtifact() {
        super("core/embedded_artifact");
    }
}

class CoreTestGroup2Repo extends DeployitIntegrationTest {
    public CoreTestGroup2Repo() {
        super("core/repo");
    }
}

class CoreTestGroup2Placeholders extends DeployitIntegrationTest {
    public CoreTestGroup2Placeholders() {
        super("core/placeholders");
    }
}

class CoreTestGroup2ResolvedPlaceholders extends DeployitIntegrationTest {
    public CoreTestGroup2ResolvedPlaceholders() {
        super("core/resolved-placeholders");
    }
}

class CoreTestGroup2DefinedPlaceholders extends DeployitIntegrationTest {
    public CoreTestGroup2DefinedPlaceholders() {
        super("core/defined-placeholders");
    }
}

class CoreTestGroup2Lock extends DeployitIntegrationTest {
    public CoreTestGroup2Lock() { super("core/lock"); }
}

class CoreTestGroup3BannerMode extends DeployitIntegrationTest {
    public CoreTestGroup3BannerMode() {
        super("core/banner");
    }
}

class CoreTestGroup3Issues extends DeployitIntegrationTest {
    public CoreTestGroup3Issues() {
        super("core/_issues");
    }
}

class CoreTestGroup3Vulnerabilities extends DeployitIntegrationTest {
    public CoreTestGroup3Vulnerabilities() {
        super("core/vulnerabilities");
    }
}

class CoreTestGroup3Checklists extends DeployitIntegrationTest {
    public CoreTestGroup3Checklists() {
        super("core/checklist");
    }
}

class CoreTestGroup3CliExtension extends DeployitIntegrationTest {
    public CoreTestGroup3CliExtension() {
        super("core/cli-extension");
    }
}

class CoreTestGroup3Config extends DeployitIntegrationTest {
    public CoreTestGroup3Config() {
        super("core/config");
    }
}

class CoreTestGroup3Conversion extends DeployitIntegrationTest {
    public CoreTestGroup3Conversion() {
        super("core/conversion");
    }
}

class CoreTestGroup3History extends DeployitIntegrationTest {
    public CoreTestGroup3History() {
        super("core/history");
    }
}

class CoreTestGroup3Reports extends DeployitIntegrationTest {
    public CoreTestGroup3Reports() {
        super("core/reports");
    }
}

class CoreTestGroup3ReportsWithPermissions extends DeployitIntegrationTest {
    public CoreTestGroup3ReportsWithPermissions() {
        super("core/reports-with-permissions");
    }
}

class CoreTestGroupHashicorpVault extends DeployitIntegrationTest {
    public CoreTestGroupHashicorpVault() {
        super("core/vault");
    }
}

class CoreTestGroupConjur extends DeployitIntegrationTest {
    public CoreTestGroupConjur() {
        super("core/conjur");
    }
}

class CoreTestGroup3Lookup extends DeployitIntegrationTest {
    public CoreTestGroup3Lookup() {
        super("core/lookup");
    }
}

class CoreTestGroup3HostCredentials extends DeployitIntegrationTest {
    public CoreTestGroup3HostCredentials() {
        super("core/host_credentials");
    }
}

class CoreTestGroup3Workers extends DeployitIntegrationTest {
    public CoreTestGroup3Workers() {
        super("core/workers");
    }
}

// Can not be run together with other tests:

class CoreTestGroupSeqPurgeTasks extends DeployitIntegrationTest {
    public CoreTestGroupSeqPurgeTasks() {
        super("core/purge-tasks");
    }
}

class CoreTestGroupSeqMaintenanceMode extends DeployitIntegrationTest {
    public CoreTestGroupSeqMaintenanceMode() {
        super("core/maintenance-mode");
    }
}

class CoreTestGroupSeqSecurityModel extends DeployitIntegrationTest {
    public CoreTestGroupSeqSecurityModel() {
        super("core/security-model");
    }
}

class CoreTestGroupSeqDefaultValues extends DeployitIntegrationTest {
    public CoreTestGroupSeqDefaultValues() {
        super("core/defaults");
    }
}

class CoreTestGroupSeqPolicy extends DeployitIntegrationTest {
    public CoreTestGroupSeqPolicy() {
        super("core/policy");
    }
}

class CoreTestGroupMQ extends DeployitIntegrationTest {
    public CoreTestGroupMQ() {
        super("core/mq");
    }
}

class CoreTestGroupSeqSupport extends DeployitIntegrationTest {
    public CoreTestGroupSeqSupport() {
        super("core/support");
    }
}

class CoreTestGroupLdap extends DeployitIntegrationTest {
    public CoreTestGroupLdap() { super("core/ldap");}
}

class ClusterTestGroup extends DeployitIntegrationTest {
    public ClusterTestGroup() { super("cluster");}
}

class TlsTestGroup extends DeployitIntegrationTest {
    public TlsTestGroup() { super("tls");}
}

class CoreTestGroupOidc extends DeployitIntegrationTest {
    public CoreTestGroupOidc() { super("core/oidc");}
}

class CoreTestGroupContextRoot extends DeployitIntegrationTest {
    public CoreTestGroupContextRoot() { super("core/contextroot");}
}
