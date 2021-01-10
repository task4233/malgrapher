ENV_TEST_FILE := .env.test
ENV_TEST := $(shell cat $(ENV_TEST_FILE))

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
run:
	gdb -q -x ./src/step.py && rm peda-session-test.txt
