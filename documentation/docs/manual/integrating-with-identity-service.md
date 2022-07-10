---
sidebar_position: 16
---

#  Manual integration with the Identity Service

## Prerequisites
- There is an account in the platform to connect to the Release instance (https://demoaccount.staging.digital.ai)
- There is an admin user (role account-admin) in the account that can be used to configure the Release client (contact Kraken team)

## 1. Adding the Release client
1. Log into the Identity Service account you want to connect to Release using an admin user for that account
2. Go to Admin > Clients > Add OIDC Client
3. Give the client a name (e.g. release)
4. Scroll down to “Valid Redirect URIs” and add
```text
<release url>/oidc-login
```
5. Save the client

## 2. Configuring Release
In CR file disable Keycloak and update OIDC properties:
```yaml
  oidc:
    enabled: true
    accessTokenUri: "https://identity.staging.digital.ai/auth/realms/demoaccount/protocol/openid-connect/token"
    clientId: "<client_id>"
    clientSecret: "<client secret>"
    emailClaim: email
    external: true
    fullNameClaim: name
    issuer: "https://identity.staging.digital.ai/auth/realms/demoaccount"
    keyRetrievalUri: "https://identity.staging.digital.ai/auth/realms/demoaccount/protocol/openid-connect/certs"
    logoutUri: "https://identity.staging.digital.ai/auth/realms/demoaccount/protocol/openid-connect/logout"
    postLogoutRedirectUri: "<release url>/oidc-login"
    redirectUri: "<release url>/oidc-login"
    rolesClaim: groups
    userAuthorizationUri: "https://identity.staging.digital.ai/auth/realms/demoaccount/protocol/openid-connect/auth"
    userNameClaim: preferred_username
    scopes: ["openid"]
```
To find the client id and secret, edit the Release client created above, scroll down to the Credentials section, and copy the values from there.

accessTokenUri, issuer, keyRetrievalUri, logoutUri, userAuthorizationUri can be found in the Identity Service UI also. There is a button 'Download OIDC config' under Clients page. These properties are saved in this conig.

## 3. Deploy Release
Deploy Release and navigate to the Release site in the browser. Use admin user from the Identity Service to log in, or create a new user in the Identity Service.
   