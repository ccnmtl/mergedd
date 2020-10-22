OUTPUT_PATH=ve
VE ?= ./ve
REQUIREMENTS ?= requirements.txt
SYS_PYTHON ?= python3
PY_SENTINAL ?= $(VE)/sentinal
WHEEL_VERSION ?= 0.34.2
PIP_VERSION ?= 20.2.4
MAX_COMPLEXITY = 7
INTERFACE ?= localhost
RUNSERVER_PORT ?= 8000
PY_DIRS ?= main

# Travis has issues here. See:
# https://github.com/travis-ci/travis-ci/issues/9524
ifeq ($(TRAVIS),true)
	FLAKE8 ?= flake8
	PIP ?= pip
	PYTEST ?= pytest
else
	FLAKE8 ?= $(VE)/bin/flake8
	PIP ?= $(VE)/bin/pip
	PYTEST ?= $(VE)/bin/pytest
endif


all: flake8 test

$(PY_SENTINAL): $(REQUIREMENTS)
	rm -rf $(VE)
	$(SYS_PYTHON) -m venv $(VE)
	$(PIP) install pip==$(PIP_VERSION)
	$(PIP) install --upgrade setuptools
	$(PIP) install wheel==$(WHEEL_VERSION)
	$(PIP) install --no-deps --requirement $(REQUIREMENTS) --no-binary cryptography
	touch $@

flake8: $(PY_SENTINAL)
	$(FLAKE8) runner.py tasks.py tests --max-complexity=$(MAX_COMPLEXITY)

test: $(PY_SENTINAL)
	$(PYTEST) tests

clean:
	rm -rf $(VE)

