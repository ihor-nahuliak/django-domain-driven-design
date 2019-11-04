.PHONY: help clean install migrate test
default: help ;

help:
	@echo 'Makefile commands:' ;\
	echo '    * make help       Shows this help information.' ;\
	echo '    * make clean      Clear local virtual environment and compiled python files.' ;\
	echo '    * make install    Install virtual environment and python libraries locally.' ;\
	echo '    * make migrate    Run all database migrations locally.' ;\
	echo '    * make test       Run unit and integration tests generating coverage report.' ;\
	echo '';


DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL=/bin/bash

GLOBAL_PYTHON = /usr/bin/python3.7
ENV := $(DIR)/env
PYTHON := $(ENV)/bin/python
PIP := $(ENV)/bin/pip
FLAKE8 := $(ENV)/bin/flake8
PYLINT := $(ENV)/bin/pylint

STATUS_INFO := \033[1;34m*\033[0m
STATUS_ERROR := \033[1;31m*\033[0m Error
STATUS_OK := \033[1;32m*\033[0m OK


clean-pyc:
	@echo -e "${STATUS_INFO} clean-pyc" ;\
	find . -name '*.pyc' -exec rm -f {} + ;\
	find . -name '*.pyo' -exec rm -f {} + ;\
	find . -name '*~' -exec rm -f {} + ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

clean: clean-pyc


install-git-hooks:
	@echo -e "${STATUS_INFO} install-git-hooks" ;\
    ln -sf $(DIR)/.githooks/pre-push $(DIR)/.git/hooks ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

install-env-python:
	@echo -e "${STATUS_INFO} install-env-python" ;\
	rm -rf "$(ENV)/" ;\
	virtualenv -p $(GLOBAL_PYTHON) --clear "$(ENV)/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

env-activate:
	@echo -e "${STATUS_INFO} env-activate" ;\
	. $(ENV)/bin/activate ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

install-python-libs:
	@echo -e "${STATUS_INFO} install-python-libs" ;\
	$(PIP) install -U pip ;\
	$(PIP) install --no-cache-dir --upgrade -r "$(DIR)/requirements.txt" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

install: install-git-hooks install-env-python env-activate install-python-libs


migrate:
	@echo -e "${STATUS_INFO} migrate" ;\
	cd "$(DIR)/app/" ;\
	DJANGO_SECRET_KEY="testing" \
	$(PYTHON) "$(DIR)/app/manage.py" migrate ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;


test-flake8:
	@echo -e "${STATUS_INFO} test-flake8" ;\
	$(FLAKE8) "$(DIR)/app/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

test-pylint:
	@echo -e "${STATUS_INFO} test-pylint" ;\
	$(PYLINT) "$(DIR)/app/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

test-unittest:
	@echo -e "${STATUS_INFO} test-unittest" ;\
	DJANGO_SECRET_KEY="testing" \
	DATABASE_NAME="project_testing" \
	$(PYTHON) "$(DIR)/app/manage.py" test "$(DIR)/app" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

test: test-unittest test-flake8 test-pylint
