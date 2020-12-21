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
# OpenDaylight docker file

FROM adoptopenjdk/openjdk11:alpine-slim AS odl

LABEL maintainer="Martin Skorupski martin.skorupski@highstreet-technologies.com"

ENV ODL_VERSION=0.13.1
ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk add bash && \
    apk add wget && \ 
    apk add --update --no-cache python3 && \
    ln -sf python3 /usr/bin/python && \
    python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools && \
    pip3 install requests && \ 
    mkdir /opt/opendaylight

WORKDIR /opt

RUN wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/opendaylight/${ODL_VERSION}/opendaylight-${ODL_VERSION}.tar.gz

RUN tar -xvzf opendaylight-${ODL_VERSION}.tar.gz -C opendaylight --strip-components 1 && \
    rm -rf opendaylight-${ODL_VERSION}.tar.gz

COPY ./org.apache.karaf.features.cfg /opt/opendaylight/etc/org.apache.karaf.features.cfg
COPY ./org.ops4j.pax.logging.cfg /opt/opendaylight/etc/org.ops4j.pax.logging.cfg

COPY ./restconf-filtering-jars/netconf-dom-api-1.9.1.jar /opt/opendaylight/system/org/opendaylight/netconf/netconf-dom-api/1.9.1/netconf-dom-api-1.9.1.jar
COPY ./restconf-filtering-jars/netconf-topology-singleton-1.9.1.jar /opt/opendaylight/system/org/opendaylight/netconf/netconf-topology-singleton/1.9.1/netconf-topology-singleton-1.9.1.jar
COPY ./restconf-filtering-jars/netconf-util-1.9.1.jar /opt/opendaylight/system/org/opendaylight/netconf/netconf-util/1.9.1/netconf-util-1.9.1.jar
COPY ./restconf-filtering-jars/restconf-common-1.12.1.jar /opt/opendaylight/system/org/opendaylight/netconf/restconf-common/1.12.1/restconf-common-1.12.1.jar
COPY ./restconf-filtering-jars/restconf-nb-rfc8040-1.12.1.jar /opt/opendaylight/system/org/opendaylight/netconf/restconf-nb-rfc8040/1.12.1/restconf-nb-rfc8040-1.12.1.jar
COPY ./restconf-filtering-jars/sal-netconf-connector-1.12.1.jar /opt/opendaylight/system/org/opendaylight/netconf/sal-netconf-connector/1.12.1/sal-netconf-connector-1.12.1.jar

COPY ./user-management-shiro/src/main/template /opt/opendaylight/configuration/config-template

COPY ./scripts /opt/opendaylight/scripts

WORKDIR /opt/opendaylight

ENV ODL_HOME=/opt/opendaylight
ENV ODL_INPUT_DIR=/opt/opendaylight/configuration/sdnr-config/
ENV ODL_TEMPLATE_DIR=/opt/opendaylight/configuration/config-template/

EXPOSE 8181

CMD ["./bin/karaf", "server"]

#DO NOT FORGET TO UPDATE KARAF FEATUURES WITH ALU SR1 hashes
