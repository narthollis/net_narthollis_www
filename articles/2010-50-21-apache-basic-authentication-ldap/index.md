---
title: Net Narthollis - Apache basic Authentication with LDAP
sitename: Net Narthollis
---
A friend asked me to share my apache LDAP authentication configuration, so I decided that if one person could use it, then so could more; so here is a snippet of my config.
<!-- more -->
~~~~{.plain}
  <Location />
    AuthBasicProvider ldap
    AuthzLDAPAuthoritative on

    AuthLDAPURL ldap://auth.example.com/dc=example,dc=com?uid
    Require valid-user
    Require ldap-group cn=admin,ou=Group,dc=example,dc=com

    AuthType Basic
    AuthName "NET NARTHOLLIS Server Admin Tools"
  </Location>
~~~~

If you have access to the apache config this this should be put there, other wise this can be put in your .htaccess file. In that case you should remove the <Location> tags.

On Gentoo Linux, it is essential to emerge apache with the 'ldap' flag enabled. Other distributions may need other various packages enabled.