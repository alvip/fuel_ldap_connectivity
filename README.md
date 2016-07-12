# fuel_ldap_connectivity
Check LDAP settings before deployment of environment, try to connect each domain LDAP server and get user and group list.

To check LDAP connectivity one should perform the following commands on fuel master node:
      
      git clone https://github.com/alvip/fuel_ldap_connectivity
      cd fuel_ldap_connectivity
      bash test_domains.sh
 
 
 
or do the same test from other location but before should set variables in openrc file. For example:
       
       git clone https://github.com/alvip/fuel_ldap_connectivity && cd fuel_ldap_connectivity

modify your openrc file:
   
       export ADDR=root@172.16.57.50
       export PWD=r00tme

and after that run the test:

      test_remote_domains.sh
 
 as result I have got output (for example):
 
      ================== DOMAIN: openldap1
      Number of users: 6
      Number of groups: 3

      ================== DOMAIN: openldap2
      Number of users: 3
      Number of groups: 3

      ================== DOMAIN: AD2
      Number of users: 11
      Number of groups: 48

      ================== DOMAIN: openldap2_new
      Number of users: 100
      Number of groups: 10
 
