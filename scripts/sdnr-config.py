#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# sdnr-config.py
#
# waits for karaf service to be up and runing before database with user related
# data can be filled. 
# karaf service will return server code 200 upon successful startup, hence script 
# continue to load users into database per RESTful API
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

import requests
from requests.auth import HTTPBasicAuth
import time
import os
import logging
logging.basicConfig(filename='./../data/log/sdnr-config.log', 
level=logging.INFO, 
format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

baseUrl = os.environ.get("ODL_BASE_URL")
path = '/auth/v1/users'
user = os.environ.get("ODL_USER")
password = os.environ.get("ODL_PASSWORD")
#thisPath = os.environ.get("AAA_SETUP_PATH")
thisPath = '.'
aaaSetupScript = thisPath + '/aaa-setup.py'
netconfTopologySetupScript = thisPath + '/netconf-topology-setup.py'

karafReady = False
print("sdnr-config.py called")
logging.info("sdnr-config.py called")
print( thisPath )

#block further execution until karaf service is ready 
while (karafReady == False):
        url = baseUrl + path
        time.sleep(20)
        print("sending reuqest")
        logging.info("sending reuqest")
        try:
            response = requests.get(url, auth=(user, password))
            response.raise_for_status()
            if response.status_code > 299:
                print('ERROR put {}'.format(response.status_code))
                logging.info('ERROR put {}'.format(response.status_code))
                if response.status_code == 401:
                    print("..looking good....waiting for Karaf ONE more time.....(otherwise better to restart)")
                    logging.info("..looking good....waiting for Karaf ONE more time.....(otherwise better to restart)")
            elif response.status_code == 200 or response.status_code == 201 or response.status_code == 204 :
                karafReady = True
            print(response.status_code)
            logging.info(response.status_code)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:",errh)
            logging.info("Http Error")
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            logging.info("Error Connecting:")
            print ("Still Waiting for Karaf.....")
            logging.info("Still Waiting for Karaf.....")
        except requests.exceptions.Timeout as errt:
            print("Timeout", errt)
            logging.info("Timeout")
        except requests.exceptions.TooManyRedirects:
            print("TooManyRedirects")
            logging.info("TooManyRedirects")
        except requests.exceptions.RequestException as e:
            print("other error: ")
            print(e)
            logging.info("other error: ")

logging.info("..karaf recognized...next AAA Setup....")

#conitnue with "loading" the daatbase
os.system('python3 ' + aaaSetupScript)
logging.info("..AAA filling oone...next NETCONF Topology Setup....")
os.system('python3 ' + netconfTopologySetupScript)
logging.info("..ready")

