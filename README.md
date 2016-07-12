# fuel_ldap_connectivity
Check LDAP settings before deployment of environment, try to connect each domain LDAP server and get user and group list.

To check LDAP connectivity one should perform the following commands on fuel master node:

 git clone https://github.com/alvip/fuel_ldap_connectivity && cd fuel_ldap_connectivity && test_domains.sh
 
 
 
or do the same test from other location but before should set variables in openrc file. For example:
 
git clone https://github.com/alvip/fuel_ldap_connectivity && cd fuel_ldap_connectivity

modify your openrc file

--- 
export ADDR=root@172.16.57.50
export PWD=r00tme
----

and after that run the test:
test_remote_domains.sh
 
 
