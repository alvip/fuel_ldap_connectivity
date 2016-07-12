#!/usr/bin/env python
import ldap
import os
import ldapurl
import pprint


def test(suffix, url, user, pwd, searchfilter="cn=*", use_tls=False, cacert=""):

    if use_tls and cacert:
	if not os.path.isfile(cacert):
	    raise IOError(_("tls_cacertfile %s not found or is not a file") % cacert)
	ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, cacert)
	#ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
	ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_HARD)
	#ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
	#ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
	# url = ldapurl.LDAPUrl(urlscheme=proto, hostport="%s:%s" % (server, str(port))).initializeUrl()

    l = ldap.initialize(url, trace_level=0)
    #l.set_option(ldap.OPT_REFERRALS, 0)
    l.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
    #l.set_option(ldap.OPT_DEBUG_LEVEL, 255 )
    #l.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
    if use_tls:
        l.start_tls_s()
    l.simple_bind_s(user, pwd)

    # baseDN = "ou=people,dc=example,dc=com"
    baseDN = suffix # "dc=%s,dc=%s" % (name, tld)
    searchScope = ldap.SCOPE_SUBTREE
    searchFilter = searchfilter # "cn=*"
    ldap_result_id = l.search(baseDN, searchScope, searchFilter)
    # pprint.pprint(l.result())
    res = l.result()
    return res

    # for i in range(ldap_result_id - 1): 
    #    print l.result(ldap_result_id, i)



if __name__ == '__main__':

    res = test(suffix='dc=mirantis,dc=tld', pwd='1111', url='ldap://172.18.196.224', use_tls=True,
               searchfilter="objectclass=inetOrgPerson", user='cn=admin,dc=mirantis,dc=tld',
               cacert='openldap1.pem')
    pprint.pprint(len(res[1]))

    res = test(suffix='dc=openldap2,dc=tld', pwd='1111', url='ldap://172.18.186.129', use_tls=False,
               searchfilter="objectclass=inetOrgPerson", user='cn=admin,dc=openldap2,dc=tld',
               cacert='openldap1.pem')
    pprint.pprint(len(res[1]))
    
    res = test(suffix='dc=openldap1,dc=tld', pwd='qwerty123!', url='ldap://172.16.56.27', use_tls=True, 
               searchfilter="objectclass=inetOrgPerson", user='cn=admin,dc=openldap1,dc=tld',
               cacert='openldap1.pem')
    pprint.pprint(len(res[1]))

