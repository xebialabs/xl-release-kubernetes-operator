package com.xebialabs.deployit.integration.test;

import com.xebialabs.deployit.util.PropertyUtil;
import org.testng.annotations.Test;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Objects;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

public class NoLicenseITest {

    private static final File serverRuntime = Objects.requireNonNull(new File("build/integration-server")
            .listFiles(file -> file.getName().startsWith("xl-deploy-") && file.getName().endsWith("-server")))[0];

    private static final File deployitConf = new File(serverRuntime.getPath() + "/conf/deployit.conf");

    private static final Integer serverPort = Integer.parseInt(PropertyUtil.readPropertiesFile(deployitConf).getProperty("http.port"));

    @Test
    public void shouldCheckProductRegistrationPage() throws URISyntaxException, IOException, InterruptedException {

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request =
                HttpRequest.newBuilder(new URI(String.format("http://localhost:%d/productregistration", serverPort)))
                        .version(HttpClient.Version.HTTP_1_1).GET().build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() == 200) {
            assertTrue("Product registration page has incorrect content.", response.body().contains("Enter your XL Deploy license"));
        } else {
            fail("Product registration page has failed to open");
        }
    }
}
