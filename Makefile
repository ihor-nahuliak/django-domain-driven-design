.PHONY: help clean install migrate test run
default: help ;

help:
	@echo 'Makefile commands (backend develop team usage only):' ;\
	echo '    * make help       Shows this help information.' ;\
	echo '    * make clean      Clear local virtual environment and compiled python files.' ;\
	echo '    * make install    Install virtual environment and python libraries locally.' ;\
	echo '                      See also: ' ;\
	echo '                          - make install-py37    Install using python 3.7 (default)' ;\
	echo '                          - make install-py38    Install using python 3.8' ;\
	echo '    * make migrate    Run all database migrations locally.' ;\
	echo '    * make test       Run unit and integration tests generating coverage report.' ;\
	echo '    * make run        Run application in development mode.' ;\
	echo '';


DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL=/bin/bash

GLOBAL_PY37 = /usr/bin/python3.7
GLOBAL_PY38 = /usr/bin/python3.8
ENV := $(DIR)/.env
PYTHON := $(ENV)/bin/python
PIP := $(ENV)/bin/pip
PEP8 := $(ENV)/bin/pycodestyle --config="$(DIR)/tox.ini"
FLAKE8 := $(ENV)/bin/flake8 --config="$(DIR)/tox.ini"
PYLINT := $(ENV)/bin/pylint --rcfile="$(DIR)/tox.ini"
MYPY := $(ENV)/bin/mypy --config-file="$(DIR)/tox.ini"
TOX := $(ENV)/bin/tox

STATUS_INFO := \r\n\033[1;94m\xF0\x9F\x91\xA3 \033[0m
STATUS_ERROR := \033[1;31m\xE2\x9C\x96\033[0m [Error]
STATUS_OK := \033[1;32m\xE2\x9C\x94\033[0m [OK]


clean-pyc:
	@echo -e "${STATUS_INFO} clean-pyc" ;\
	find . -name '*.pyc' -exec rm -f {} + ;\
	find . -name '*.pyo' -exec rm -f {} + ;\
	find . -name '*~' -exec rm -f {} + ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

clean: clean-pyc


install-git-hooks:
	@echo -e "${STATUS_INFO} install-git-hooks" ;\
    ln -sf $(DIR)/.githooks/pre-push $(DIR)/.git/hooks ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

install-env-py37:
	@echo -e "${STATUS_INFO} install-env-py37" ;\
	rm -rf "$(ENV)/" ;\
	virtualenv -p $(GLOBAL_PY37) --clear "$(ENV)/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

install-env-py38:
	@echo -e "${STATUS_INFO} install-env-py38" ;\
	rm -rf "$(ENV)/" ;\
	virtualenv -p $(GLOBAL_PY38) --clear "$(ENV)/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

env-activate:
	@echo -e "${STATUS_INFO} env-activate" ;\
	. $(ENV)/bin/activate ;\
	$(PYTHON) --version ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

install-python-libs:
	@echo -e "${STATUS_INFO} install-python-libs" ;\
	$(PYTHON) -Im ensurepip --upgrade --default-pip ;\
	$(PIP) install -U pip ;\
	$(PIP) install --no-cache-dir --upgrade -r "$(DIR)/requirements.txt" ;\
	$(PIP) install --no-cache-dir --upgrade -r "$(DIR)/requirements_tests.txt" ;\
	echo -e "-------------------------------------------------------------" ;\
	$(PIP) freeze ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

install-py37: install-git-hooks install-env-py37 env-activate install-python-libs

install-py38: install-git-hooks install-env-py38 env-activate install-python-libs

install: install-py37


migrate:
	@echo -e "${STATUS_INFO} migrate" ;\
	cd "$(DIR)/app/" ;\
	$(PYTHON) "$(DIR)/app/manage.py" migrate ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-pep8:
	@echo -e "${STATUS_INFO} test-pep8" ;\
	$(PEP8) --version ;\
	$(PEP8) "$(DIR)/app/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-flake8:
	@echo -e "${STATUS_INFO} test-flake8" ;\
	$(FLAKE8) --version ;\
	$(FLAKE8) "$(DIR)/app/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-pylint:
	@echo -e "${STATUS_INFO} test-pylint" ;\
	$(PYLINT) --version ;\
	$(PYLINT) "$(DIR)/app/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-mypy:
	@echo -e "${STATUS_INFO} test-mypy" ;\
	$(MYPY) --version ;\
	$(MYPY) "$(DIR)/app";\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-unittest:
	@echo -e "${STATUS_INFO} test-unittest" ;\
	$(PYTHON) "$(DIR)/app/manage.py" test "$(DIR)/app" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-tox:
	@echo -e "${STATUS_INFO} test-tox" ;\
	$(TOX) ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test: test-unittest test-pep8 test-flake8 test-mypy test-pylint


install-create-superuser:
	@echo -e "${STATUS_INFO} install-create-superuser" ;\
	echo -e 'User: admin ' ;\
	echo -e 'Pass: admin ' ;\
	echo "\
        from django.contrib.auth import get_user_model; \
        User = get_user_model(); \
        User.objects.filter(email='admin@localhost', is_superuser=True).delete(); \
        User.objects.create_superuser('admin', 'admin@localhost', 'admin'); \
	" | \
	DJANGO_DEBUG=1 \
	$(PYTHON) "$(DIR)/app/manage.py" shell ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

run-server:
	@echo -e "${STATUS_INFO} run" ;\
	DJANGO_DEBUG=1 \
	$(PYTHON) "$(DIR)/app/manage.py" runserver ;\
	if [ $$? -ne 0 ]; then \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

run: install-create-superuser run-server
