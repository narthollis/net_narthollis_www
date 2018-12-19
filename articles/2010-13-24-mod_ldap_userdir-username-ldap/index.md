---
title: Net Narthollis - mod_ldap_userdir - ~username with LDAP
sitename: Net Narthollis
---
Recently I had a need to put up some code that didn't reallydeserve its own sub domain. It was some testing code that I wanted to make public to get an idea of how it worked. My normal solution in this case would be to just use my ~/public_html/ folder. But as my normal user on the server doesn't exist in /etc/passwd this caused a slight issue...

Enter mod_ldap_userdir.

mod_ldap_userdir is an apache module that reads the users from an LDAP directory rather than from the local user list (/etc/passwd or the like). Configuring it to work is a bit more involved mod_userdir (as expected really... it can't exactly magically guess where you LDAP directory is now can it)

There are two key points to making sure it works, the first is ensuring you have all of the LDAP options configured correctly eg.
~~~~.apache
LDAPUserDirServerURL    ldap://auth.domain.tld/ou%3DPeople%2Cdc%3domain%2Cdc%3Dtld??sub?(&(uid=%25u)(objectClass=posixAccount))
LDAPUserDir             public_html
~~~~
or the more readable style (that I didn't get working, YMMV)
~~~~.apache
LDAPUserDirServer    auth.domain.tld
LDAPUserDirBaseDN    "ou=People,dc=domain,dc=tld"
LDAPUserDirFilter    "(&(uid=%u)(objectClass=posixAccount))"
LDAPUserDir          public_html
~~~~

The other key point is to ensure that the ~public_html folders have the correct apache permissions. This is the big place I stuffed up, as mod_ldap_userdir dosn't work if mod_userdir is loaded, and all of the folder permissions are stored in the mod_userdir config (in gentoo at lease).

~~~~.apache

# Control access to UserDir directories.  The following is an example
# for a site where these directories are restricted to read-only.
<Directory /home/*/public_html>
  AllowOverride FileInfo AuthConfig Limit Indexes
  Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec
  <Limit GET POST OPTIONS>
    Order allow,deny
    Allow from all
  </Limit>
  <LimitExcept GET POST OPTIONS>
    Order deny,allow
    Deny from all
  </LimitExcept>
</Directory>

# Suexec isn't really required to run cgi-scripts, but it's a really good
# idea if you have multiple users serving websites...
<IfDefine SUEXEC>
  <Directory /home/*/public_html/cgi-bin>
    Options ExecCGI
    SetHandler cgi-script
  </Directory>
</IfDefine>

</IfDefine>
~~~~

I hope this helps you, if you ever have need of userdir's in an LDAP enviroment.