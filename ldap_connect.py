#!/usr/bin/env python

import yaml
import pprint
import check_ldap

def show_error(ldap_set, domain_name, e, objectclass=''):
    print 'suffix=%s' % ldap_set['suffix']
    print 'url=%s' % ldap_set['url']
    print 'user=%s' % ldap_set['user']
    print 'password=%s' % ldap_set['password']
    print 'use_tls=%s' % ldap_set['use_tls']
    print 'searchfilter=%s' % ldap_set[objectclass]
    print 'cacert=%s.pem' % domain_name
    print "Error: %s\n" % e


with open('settings.yaml', 'r') as f:
    doc = yaml.load(f)

res = doc['editable']['ldap']

# select ldap settings and save them in ldap.yaml file
with open('ldap.yaml', 'w') as yaml_file:
    yaml_file.write( yaml.dump(res, default_flow_style=False))

domain_list = []

# save parameters from the basic settings in domain.basic file
root =  res['metadata']['versions'][0]
domain = root['domain']['value']
domain_list.append(domain)
with open('domain.%s' % domain, 'w') as f2:
    root =  res['metadata']['versions'][0]
    param_list = [
        'domain', 'group_desc_attribute',
        'group_filter', 'group_id_attribute', 'group_member_attribute',
        'group_name_attribute', 'group_objectclass', 'group_tree_dn',
        'ldap_proxy',  'page_size', # 'ldap_proxy_custom_conf',
        'password', 'query_scope', 'suffix', 'url', 'use_tls', 'user',
        'user_enabled_attribute', 'user_filter', 'user_id_attribute',
        'user_name_attribute', 'user_objectclass', 'user_pass_attribute',
        'user_tree_dn', 'chase_referrals', 'ca_chain' ]
    for r in param_list:
        f2.write('%s=%s\n' % (r, root[r]['value']))

# parse yaml file and save parameters of the additional domains in the separate files
data = res['metadata']['versions'][0]['additional_domains']['value']
kv_list = data.split('\n')
# pprint.pprint(kv_list)

fd = open('/dev/null', 'w')
name = 'none'
flag = False
for line in kv_list:
    if 'domain' in line:
        name = line.split('=')[1]
        domain_list.append(name)
        fd.close()
        fd = open('domain.%s' % name, 'w')
    fd.write('%s\n' % line)
fd.close()


# save certificate in *.pem file
for domain_name in domain_list:
    with open('domain.%s' % domain_name, 'r') as f:
        lines=f.readlines()
        for line in lines:
            if '-----BEGIN CERTIFICATE-----' in line:
                fcert = open('%s.pem' % domain_name, 'w')
                line = line.split('=')[1]
                flag = True 
            if flag:
                fcert.write('%s' % line)             
            if '-----END CERTIFICATE-----' in line:
                flag = False
                fcert.close() 

# connect ldap server and analyze user and group list
for domain_name in domain_list:

    with open('domain.%s' % domain_name, 'r') as f:
        lines=f.readlines()
        ldap_set = {}
        for l in lines:
            lnew = l.strip()
            pair = lnew.split('=')
            key = pair[0]
            value = '='.join(pair[1:])
            for p in ['domain', 'url', 'user', 'password', 'suffix', 'user_objectclass', 'group_objectclass', 'use_tls']:
                if p == key: ldap_set[p] = value

        # pprint.pprint(ldap_set)
        print "\n================== DOMAIN: %s" % ldap_set['domain']
        if ldap_set['use_tls'].lower() == 'true':
             ldap_set['use_tls'] = True
        else:
             ldap_set['use_tls'] = False

        try:
            users = check_ldap.test(suffix=ldap_set['suffix'],
                        url = ldap_set['url'],
                        user = ldap_set['user'],
                        pwd = ldap_set['password'],
                        searchfilter = 'objectclass=%s' % ldap_set['user_objectclass'], # 'cn=groupOfNames', # 'inetOrgPerson',
                        use_tls = ldap_set['use_tls'],
                        cacert = '%s.pem' % domain_name)
            print "Number of users: %s" % len(users[1])
        except Exception as e:
            show_error(ldap_set, domain_name, e, 'user_objectclass')

        try:
            groups = check_ldap.test(suffix=ldap_set['suffix'],
                        url=ldap_set['url'],
                        user=ldap_set['user'],
                        pwd=ldap_set['password'],
                        searchfilter = 'objectclass=%s' % ldap_set['group_objectclass'], # 'cn=groupOfNames', # 'inetOrgPerson',
                        use_tls = ldap_set['use_tls'],
                        cacert = '%s.pem' % domain_name)
            print "Number of groups: %s" % len(groups[1])
        except Exception as e:
            show_error(ldap_set, domain_name, e, 'group_objectclass')


