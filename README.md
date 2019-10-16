# django-domain-driven-design
[![Build Status](https://travis-ci.org/ihor-nahuliak/django-domain-driven-design.svg?branch=master)](https://travis-ci.org/ihor-nahuliak/django-domain-driven-design)
[![Coverage Status](https://coveralls.io/repos/github/ihor-nahuliak/django-domain-driven-design/badge.svg)](https://coveralls.io/github/ihor-nahuliak/django-domain-driven-design)

django domain driven design example


### Installation

Dependencies:

    * ubuntu 16.04
    * python3.7
    * python3.7-dev
    * postgresql-9.6
    * postgresql-client-9.6
    * postgresql-contrib-9.6
    * postgresql-9.6-postgis-scripts

To install python 3.7 please do:
```
sudo add-apt-repository -y ppa:deadsnakes/ppa &&\
sudo apt-get update &&\
sudo apt-get install -y python3.7 python3.7-dev
```

To install postgresql 9.6 and required extensions please do:
```
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - &&\
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list &&\
sudo apt-get update &&\
sudo apt-get install -y \
postgresql-9.6 \
postgresql-client-9.6 \
postgresql-contrib-9.6 \
postgresql-9.6-postgis-scripts
```

To create database with required extensions please do:
```
sudo -u postgres psql -U postgres -c 'create database project;' &&\
sudo -u postgres psql -d project -U postgres -c 'create extension postgis;'
```

To migrate local database run: ```make migrate```

To install python environment locally run: ```make install```

To see additional options run: ```make help```


### Testing

To execute tests locally run: ```make test```

To see additional options run: ```make help```
