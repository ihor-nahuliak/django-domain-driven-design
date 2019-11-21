.PHONY: help clean install migrate test run
default: help ;

help:
	@echo 'Makefile commands:' ;\
	echo '    * make help       Shows this help information.' ;\
	echo '    * make clean      Clear local virtual environment and compiled python files.' ;\
	echo '    * make install    Install virtual environment and python libraries locally.' ;\
	echo '    * make migrate    Run all database migrations locally.' ;\
	echo '    * make test       Run unit and integration tests generating coverage report.' ;\
	echo '    * make run        Run application in development mode.' ;\
	echo '';


DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL=/bin/bash

GLOBAL_PYTHON_PY37 = /usr/bin/python3.7
GLOBAL_PYTHON_PY38 = /usr/bin/python3.8
ENV := $(DIR)/env
PYTHON := $(ENV)/bin/python
PIP := $(ENV)/bin/pip
TOX := $(ENV)/bin/tox -c="$(DIR)/tox.ini"

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

install-env-python-py37:
	@echo -e "${STATUS_INFO} install-env-python-py37" ;\
	rm -rf "$(ENV)/" ;\
	virtualenv -p $(GLOBAL_PYTHON_PY37) --clear "$(ENV)/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

install-env-python-py38:
	@echo -e "${STATUS_INFO} install-env-python-py38" ;\
	rm -rf "$(ENV)/" ;\
	virtualenv -p $(GLOBAL_PYTHON_PY38) --clear "$(ENV)/" ;\
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
	$(PIP) install -U pip ;\
	$(PIP) install --no-cache-dir --upgrade -r "$(DIR)/requirements.txt" ;\
	echo -e "-------------------------------------------------------------" ;\
	$(PIP) freeze ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

install: install-git-hooks install-env-python-py37 env-activate install-python-libs


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
	$(TOX) -e=pycodestyle ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-flake8:
	@echo -e "${STATUS_INFO} test-flake8" ;\
	$(TOX) -e=flake8 ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-pylint:
	@echo -e "${STATUS_INFO} test-pylint" ;\
	$(TOX) -e=pylint ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-mypy:
	@echo -e "${STATUS_INFO} test-mypy" ;\
	$(TOX) -e=mypy ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
		exit 1 ;\
	fi;

test-unittest:
	@echo -e "${STATUS_INFO} test-unittest" ;\
	$(TOX) -e=py37 ;\
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
