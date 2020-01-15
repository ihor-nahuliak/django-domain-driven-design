# django-domain-driven-design
[![Build Status](https://travis-ci.org/ihor-nahuliak/django-domain-driven-design.svg?branch=master)](https://travis-ci.org/ihor-nahuliak/django-domain-driven-design)
[![Coverage Status](https://coveralls.io/repos/github/ihor-nahuliak/django-domain-driven-design/badge.svg)](https://coveralls.io/github/ihor-nahuliak/django-domain-driven-design)

django domain driven design example


### Installation

Dependencies:

    * ubuntu 16.04
    * python3.7
    * python3.7-dev
    * python3.7-venv
    * python3.7-distutils
    * python3.8
    * python3.8-dev
    * python3.8-venv
    * python3.8-distutils
    * postgresql-10
    * postgresql-client-10
    * postgresql-contrib-10
    * postgresql-10-postgis-scripts

To install python 3.7 please do:
```shell script
sudo add-apt-repository -y ppa:deadsnakes/ppa &&\
sudo apt-get update &&\
sudo apt-get install -y python3.7 python3.7-dev &&\
python3.7 --version
```

To install python 3.8 please do:
```shell script
sudo add-apt-repository -y ppa:deadsnakes/ppa &&\
sudo apt-get update &&\
sudo apt-get install -y python3.8 python3.8-dev &&\
python3.8 --version
```

To install postgresql 10 and required extensions please do:
```shell script
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - &&\
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list &&\
sudo apt-get update &&\
sudo apt-get install -y \
postgresql-10 \
postgresql-client-10 \
postgresql-contrib-10 \
postgresql-10-postgis-scripts &&\
psql --version
```

To create database with required extensions please do:
```shell script
sudo -u postgres psql -U postgres -c 'create database project;' &&\
sudo -u postgres psql -d project -U postgres -c 'create extension postgis;'
```

The same using postgresql-postgis docker-image:
```shell script
docker run --name postgresql -itd --restart always \
  -p 5432:5432 \
  --env 'POSTGRES_USER=postgres' \
  --env 'POSTGRES_PASSWORD=' \
  --env 'POSTGRES_DB=project' \
  corpusops/postgis-bare:10-2.5-alpine
```

To migrate local database run: ```make migrate```

To install python environment locally run: ```make install```

To see additional options run: ```make help```


### Testing

To execute tests locally run: ```make test```
You also can use tox: ```tox```

To see additional options run: ```make help```
