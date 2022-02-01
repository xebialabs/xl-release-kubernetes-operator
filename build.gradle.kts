import com.github.gradle.node.yarn.task.YarnTask
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

buildscript {
    repositories {
        mavenLocal()
        gradlePluginPortal()
        arrayOf("releases", "public").forEach { r ->
            maven {
                url = uri("${project.property("nexusBaseUrl")}/repositories/${r}")
                credentials {
                    username = project.property("nexusUserName").toString()
                    password = project.property("nexusPassword").toString()
                }
            }
        }
    }

    dependencies {
        classpath("com.xebialabs.gradle.plugins:gradle-commit:${properties["gradleCommitPluginVersion"]}")
        classpath("com.xebialabs.gradle.plugins:gradle-xl-defaults-plugin:${properties["xlDefaultsPluginVersion"]}")
        classpath("com.xebialabs.gradle.plugins:gradle-xl-plugins-plugin:${properties["xlPluginsPluginVersion"]}")
        classpath("com.xebialabs.gradle.plugins:integration-server-gradle-plugin:${properties["integrationServerGradlePluginVersion"]}")
    }
}

plugins {
    kotlin("jvm") version "1.4.20"

    id("com.github.node-gradle.node") version "3.1.0"
    id("idea")
    id("nebula.release") version "15.3.1"
    id("maven-publish")
}

apply(plugin = "integration.server")
apply(plugin = "ai.digital.gradle-commit")
apply(plugin = "com.xebialabs.dependency")

apply(from = "$rootDir/integration-tests/base-test-configuration.gradle")

group = "ai.digital.release.operator"
project.defaultTasks = listOf("build")

val definedOperatorVersion = System.getenv()["OPERATOR_VERSION"]

val releasedVersion = "22.0.0-${LocalDateTime.now().format(DateTimeFormatter.ofPattern("Mdd.Hmm"))}"
project.extra.set("releasedVersion", definedOperatorVersion ?: releasedVersion)

repositories {
    mavenLocal()
    gradlePluginPortal()
    maven {
        url = uri("https://plugins.gradle.org/m2/")
    }
}

idea {
    module {
        setDownloadJavadoc(true)
        setDownloadSources(true)
    }
}

dependencies {
    implementation(gradleApi())
    implementation(gradleKotlinDsl())

}

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

tasks.named<Test>("test") {
    useJUnitPlatform()
}

tasks {
    named<YarnTask>("yarn_install") {
        args.set(listOf("--mutex", "network"))
        workingDir.set(file("${rootDir}/documentation"))
    }

    for (suffix in listOf("aws-eks", "azure-aks", "gcp-gke", "onprem", "openshift")) {
        register<Zip>("operatorArchives${suffix.capitalize().replace("-", "")}") {
            from("release-operator-$suffix") {
                include("**/*")
                archiveBaseName.set("release-operator-${suffix}")
                archiveVersion.set(releasedVersion)
            }
        }
    }

    register<YarnTask>("yarnRunStart") {
        dependsOn(named("yarn_install"))
        args.set(listOf("run", "start"))
        workingDir.set(file("${rootDir}/documentation"))
    }

    register<YarnTask>("yarnRunBuild") {
        dependsOn(named("yarn_install"))
        args.set(listOf("run", "build"))
        workingDir.set(file("${rootDir}/documentation"))
    }

    register<Delete>("docCleanUp") {
        delete(file("${rootDir}/docs"))
        delete(file("${rootDir}/documentation/build"))
        delete(file("${rootDir}/documentation/.docusaurus"))
        delete(file("${rootDir}/documentation/node_modules"))
    }

    register<Copy>("docBuild") {
        dependsOn(named("yarnRunBuild"), named("docCleanUp"))
        from(file("${rootDir}/documentation/build"))
        into(file("${rootDir}/docs"))
    }

    register<GenerateDocumentation>("updateDocs") {
        dependsOn(named("docBuild"))
    }

    register<NebulaRelease>("nebulaRelease") {
        dependsOn(named("updateDocs"))
    }

    named<Upload>("uploadArchives") {
        dependsOn(named("publish"))
    }

    compileKotlin {
        kotlinOptions.jvmTarget = JavaVersion.VERSION_11.toString()
    }

    compileTestKotlin {
        kotlinOptions.jvmTarget = JavaVersion.VERSION_11.toString()
    }

    withType<PublishToMavenRepository> {
        dependsOn("operatorArchivesAwseks")
    }
}

publishing {
    publications {
        for (suffix in listOf("aws-eks", "azure-aks", "gcp-gke", "onprem", "openshift")) {
            register<MavenPublication>("dist-$suffix") {
                artifact(tasks["operatorArchives${suffix.capitalize().replace("-", "")}"])
                artifactId = "release-operator-$suffix"
                version = releasedVersion
            }
        }
    }
    repositories {
        maven {
            url = uri("${project.property("nexusBaseUrl")}/repositories/releases")
            credentials {
                username = project.property("nexusUserName").toString()
                password = project.property("nexusPassword").toString()
            }
        }
    }
}

node {
    version.set("16.13.2")
    yarnVersion.set("1.22.17")
    download.set(true)
}
