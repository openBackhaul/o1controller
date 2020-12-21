# o1controller
- OpenDaylight based SDN Controller, which is used in the ONAP and the TSI project.
- Martin Skorupski (Martin.Skorupski@openBackhaul.com)

### Branch
- 1.0.0-tsi.d.t : Version as it is used in the Transport SDN Introduction project at Telefonica Germany.

### Open Issue List
- [o1controller/issues](../../issues)

### Comments
./.


Installation and usage
----------------------

## Prerequisites

### Docker

Docker needs to be installed on the host machine where the SDN-R will be deployed. More information on installing Docker [here](https://docs.docker.com/get-docker/).

Summary for Ubuntu installation:

```console
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Docker-compose

Docker-compose is required on the host machine where the SDN-R will run. More information on installing docker-compose [here](https://docs.docker.com/compose/install/).

Summary for Ubuntu installation:

```console
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

## Installation

From the base folder:

```bash
docker-compose build
```

This will create a new Docker image containing the SDN-R. It can be verified with:

```bash
└─ $ ▶ docker images | grep onap-sdnr
onap-sdnr                                            0.8.1                   5a9bf59c02c8        19 hours ago        918MB

```

## Usage

### Configuration

The folder **deploy/sdnr-config** contains AAA and Netconf Topology configurations that can be pre-loaded into SDN-R. Both types of configuration use *.csv files to describe data to be loaded. Please use the provided files as examples and do not alter the csv columns description if you want to use them.

### Starting

SDN-R will have by default *admin/admin* as credentials. Before starting, the user has the responsibility of setting **ODL_USERNAME** and **ODL_PASSWORD** as environment variables on the host machine, containing the credentials. Example for Ubuntu machine:

```bash
export ODL_USERNAME=admin
export ODL_PASSWORD=admin
```

Then, from the base folder:

```bash
cd deploy

docker-compose up -d
```

This will start an SDN-R instance in the background. It can be verified with:

```bash
└─ $ ▶ docker ps
CONTAINER ID        IMAGE                                                COMMAND                  CREATED             STATUS              PORTS                                                                               NAMES
d8a35b708406        onap-sdnr:0.8.1                                      "/opt/opendaylight/s…"   6 seconds ago       Up 5 seconds        0.0.0.0:8181->8181/tcp                                                              sdnr

```