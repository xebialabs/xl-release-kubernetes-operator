configInfo = proxies.configuration.properties

assertEquals('true', configInfo['client.automatically.map.all.deployables'])
assertEquals('true', configInfo['client.session.remember.enabled'])
assertEquals('20', configInfo['client.session.timeout.minutes'])
