PLATFORM = $(shell uname)

PROJECT_NAME=set-destiny-web
PROJECT_TAG?=set-destiny-web

VIRTUALENV_ARGS=-p python3.6

PYTHON_MODULES=set_destiny_web

WGET = wget -q

ifeq "" "$(shell which wget)"
WGET = curl -O -s -L
endif

OK=\033[32m[OK]\033[39m
FAIL=\033[31m[FAIL]\033[39m
CHECK=@if [ $$? -eq 0 ]; then echo "${OK}"; else echo "${FAIL}" ; fi

default: test

include python.mk

clean: python_clean

purge: python_purge

build: python_build ${CHECKPOINT_DIR}/.python_develop

run: build
	${VIRTUALENV} FLASK_ENV=development FLASK_APP=set_destiny_web.main flask run

worker: build
	${VIRTUALENV} celery -A set_destiny_web.background.main worker -l INFO --no-execv


test: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} py.test ${PYTHON_MODULES} --ignore ${PYTHON_MODULES}/tests/integration

pdb: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} CI=1 py.test ${PYTHON_MODULES} -x --ff --pdb --ignore ${PYTHON_MODULES}/test/integration

coverage: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} CI=1 py.test ${PYTHON_MODULES} --cov=${PYTHON_MODULES} ${PYTHON_MODULES}/test/ --cov-config .coveragerc --cov-report term-missing --cov-report html:cov_html --cov-report xml:cov.xml --cov-report annotate:cov_annotate

codestyle: ${REQUIREMENTS_TEST}
	${VIRTUALENV} pycodestyle --statistics -qq ${PYTHON_MODULES} | sort -rn || echo ''

todo: ${REQUIREMENTS_TEST}
	${VIRTUALENV} flake8 ${PYTHON_MODULES}
	${VIRTUALENV} pycodestyle --first ${PYTHON_MODULES}
	find ${PYTHON_MODULES} -type f | xargs -I [] grep -H TODO []

search:
	find ${PYTHON_MODULES} -regex .*\.py$ | xargs -I [] egrep -H -n 'print|ipdb' [] || echo ''

dist: python_egg python_wheel


.PHONY: clean purge dist
