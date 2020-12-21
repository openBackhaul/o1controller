#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# netconf-topology-setup.py
#
# adds NE's to odl and verifies the result
#
# Copyright 2020 highstreet technologies GmbH and others
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import os
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
from string import Template
import codecs
import csv
import json
import logging
logging.basicConfig(filename='netconf-topology-setup.log', 
level=logging.INFO, 
format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')


baseUrl = os.environ.get("ODL_BASE_URL")
user = os.environ.get("ODL_USER")
password = os.environ.get("ODL_PASSWORD")
inputDir = os.environ.get("ODL_INPUT_DIR") + 'netconf-topology/'
templateDir = os.environ.get("ODL_TEMPLATE_DIR")

putPath = '/rests/data/network-topology:network-topology/topology=topology-netconf/node='
getPath = '/rests/data/network-topology:network-topology/topology=topology-netconf'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


# defining own template such that field names can have white spaces 
class MyTemplate(Template):
   delimiter = '$'
   idpattern = '[_a-z][\s_a-z0-9]*'

template = open( templateDir + 'mount-point.template')
body = MyTemplate(template.read())
defaults = {"Username": "admin", "Password": "admin", "RequestTimeout": 900000, "ReconnectOnSchemaChange": "false", "MaxConnAttempts": 3, "RpcLimit": 0, "TcpOnly": "false", "KeepAliveDelay": 120}

failureCount = 0
successCount = 0
rowCount = 0
NUM_OF_ROWS_TO_READ = int(os.environ.get("SDNR_MOUNTPOINT_COUNT"))

for filename in os.listdir(inputDir):
    if filename.endswith(".csv"): 
        with codecs.open(os.path.join(inputDir, filename), 'r', encoding='utf-8', errors='ignore') as input:
            with input as csvFile:
                csvReader = csv.DictReader(csvFile, delimiter=';')
                print("Parsing file: ", filename)
                rowCount = 0
                for row in csvReader:
                    print("adding Mountpoint: ", row['Mountname'], " IP: ", row['MPAddress'] , " port: ", row['NetconfPort'] )
                    logging.info('adding Mountpoint %s with IP %s and port %s', row['Mountname'], row['MPAddress'], row['NetconfPort'])

                    findReplace = defaults
                    for column in csvReader.fieldnames:
                        findReplace[column] = row[column]

                    data = json.loads(body.substitute(findReplace))
                    url = baseUrl + putPath + row['Mountname']

                    response = requests.put(url,headers = headers,auth = HTTPBasicAuth(user, password), json = data)

                    print('Response: ', response.status_code)
                    logging.info('server response code: %d', response.status_code)

                    if response.status_code > 299:
                        failureCount +=1
                    else:
                        successCount +=1
                    rowCount +=1
                    
                    if (NUM_OF_ROWS_TO_READ > 0) and (rowCount >= NUM_OF_ROWS_TO_READ):
                        break
    else:
        continue


#verify: 
url = baseUrl + getPath
response = requests.get(url,auth = HTTPBasicAuth(user, password))
logging.info('verification - server response code: %d', response.status_code)
logging.info(json.dumps(response.text, indent=4, sort_keys=True))
print("##########################################")
print("successful mounts: ", successCount)
logging.info("successful mounts: %d", successCount)
print("failed mounts: ", failureCount)
logging.info("failed mounts: %d", failureCount)
print("##########################################")
