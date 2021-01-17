ENV_TEST_FILE := .env.test
ENV_TEST := $(shell cat $(ENV_TEST_FILE))

ENV_TARGET_FILE := target/test32
# ENV_TARGET := $(shell cat $(ENV_TARGET_FILE))

.PHONY:gen32
gen32:
	gcc -m32 -o ./target/test32 ./target/test.c

.PHONY:gen
gen:
	gcc -o ./target/test ./target/test.c

.PHONY:test
test:
	$(ENV_TEST) coverage run --source ./makecfg -m unittest discover ./tests
	coverage report -m

.PHONY:run
run:gdb -q -x ./src/step.py && rm peda-session-test.txt

showmain:
	$(ENV_TEST) gdb -batch -ex "file ${ENV_TARGET_FILE}" -ex 'disassemble main'

createcfg:
	$(ENV_TEST) gdb -q -x ./gdb_scripts/make_cfg.py $(ENV_TARGET_FILE)