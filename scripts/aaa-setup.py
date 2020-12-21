#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
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
import urllib.parse
from string import Template
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

baseUrl = os.environ.get("ODL_BASE_URL")
user = os.environ.get("ODL_USER")
password = os.environ.get("ODL_PASSWORD")
inputDir = os.environ.get("ODL_INPUT_DIR") + 'aaa/'
templateDir = os.environ.get("ODL_TEMPLATE_DIR")
headers = {'Content-type': 'application/json',
           'Accept': 'application/json'}

# users
print("Users log: \n")

path = '/auth/v1/users'
template = open( templateDir + 'user.template')
input = open( inputDir + 'users.csv', newline='')
body = Template(template.read())

with input as csvFile:
    csvReader = csv.DictReader(csvFile)

    for row in csvReader:
        print(row['NAME'], ": ", row['DESCRIPTION'], "adding ...")
        # create substitute mapping in json
        findReplace = {}
        for column in csvReader.fieldnames:
            findReplace[column] = row[column]

        url = baseUrl + path
        data = json.loads(body.substitute(findReplace))
        response = requests.post(url, headers=headers, auth=HTTPBasicAuth(user, password), json=data)

        if response.status_code > 299:
            print('ERROR put {}'.format(response.status_code))
        print(row['NAME'], response.status_code)

# roles
print("\nRoles log:")

path = '/auth/v1/roles/'
template = open( templateDir + 'role.template')
input = open( inputDir + 'roles.csv', newline='')
body = Template(template.read())

with input as csvFile:
    csvReader = csv.DictReader(csvFile)

    for row in csvReader:
        print(row['NAME'], "adding ...")
        # create substitute mapping in json
        findReplace = {}
        for column in csvReader.fieldnames:
            findReplace[column] = row[column]

        url = baseUrl + path
        data = json.loads(body.substitute(findReplace))
        response = requests.post(url, headers=headers, auth=HTTPBasicAuth(user, password), json=data)

        if response.status_code > 299:
            print('ERROR PUT {}'.format(response.status_code))
        print(row['NAME'], response.status_code)

# grants
print("\nGrants log:")

path = '/auth/v1/domains/'
template = open( templateDir + 'grant.template')
input = open( inputDir + 'grants.csv', newline='')
body = Template(template.read())

with input as csvFile:
    csvReader = csv.DictReader(csvFile)

    for row in csvReader:
        print(row['ID'], ": ", row['NAME'], "adding ...")
        # create substitute mapping in json
        findReplace = {}
        for column in csvReader.fieldnames:
            findReplace[column] = row[column]

        url = baseUrl + path + row['DOMAIN'] + "/users/" + row['NAME'] + "@" + row['DOMAIN'] + "/roles"
        data = json.loads(body.substitute(findReplace))
        response = requests.post(url, headers=headers, auth=HTTPBasicAuth(user, password), json=data)

        if response.status_code > 299:
            print('ERROR PUT {}'.format(response.status_code))
        print(row['NAME'], response.status_code)

# policies
# - this is using md-sal, shiro offers just static authorization
print("\nPolicies log:")

path = '/rests/data/aaa:http-authorization/policies'

try:
    body = open( inputDir + 'aaa-app-config-rest.json')
    data = json.load(body)
    url = baseUrl + path

    response = requests.put(url, headers=headers, auth=HTTPBasicAuth(user, password), json=data)

    if response.status_code > 299:
        print('ERROR PUT {}'.format(url, response.status_code))
    print('Policies returned status: ', response.status_code)
except FileNotFoundError:
    print("Error: input/aaa-app-config-rest.json not found!")
