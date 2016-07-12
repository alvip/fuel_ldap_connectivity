#!/bin/bash

# set -x

export ENV_IDS=`fuel env | tail -n +3 | awk '{printf "%4d ",$1}'`
echo 'List of current enviroments: ' $ENV_IDS


for ENV_ID in $ENV_IDS
do
 clean_up.sh
 echo analyzing ENV_ID=$ENV_ID

 mkdir /tmp/fuel_settings
 fuel settings --download --env-id=$ENV_ID --dir /tmp/fuel_settings
 cp /tmp/fuel_settings/settings_$ENV_ID.yaml settings.yaml
 python ldap_connect.py
done
        
