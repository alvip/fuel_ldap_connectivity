#!/bin/bash

# set -x
. openrc
export OPTS="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

# sshpass -p $PWD ssh $OPTS $ADDR "ls"
# sshpass -p $PWD ssh $OPTS $ADDR "fuel env | tail -n +3 | awk '{printf \"%4d \",$1}'"
export ENV_IDS=`sshpass -p $PWD ssh $OPTS $ADDR "fuel env | tail -n +3" | awk '{printf "%4d ",$1}'`
echo 'List of current enviroments: ' $ENV_IDS 

for ENV_ID in $ENV_IDS
do
 echo analyzing ENV_ID=$ENV_ID
 rm settings.yaml
 rm domains.*
 rm *.pem

 sshpass -p $PWD ssh $OPTS $ADDR "mkdir /tmp/fuel_settings"
 sshpass -p $PWD ssh $OPTS $ADDR "fuel settings --download --env-id=$ENV_ID --dir /tmp/fuel_settings"
 sshpass -p $PWD scp $OPTS $ADDR:/tmp/fuel_settings/settings_$ENV_ID.yaml settings.yaml
 python ldap_connect.py
done

