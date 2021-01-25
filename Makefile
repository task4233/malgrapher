ENV_TEST_FILE := .env.test
ENV_TEST := $(shell cat $(ENV_TEST_FILE))

.PHONY: build
build:
	docker build . -t makecfg/latest

.PHONY: run
run:
	docker run -it --name makecfg --rm makecfg/latest 

.PHONY: out
out:
	rm -f ./cfg.png
	docker run -it --rm -v ./out:/tmp/ --name makecfg makecfg/latest

.PHONY: up
up:
	go run . &

createcfg:
	$(ENV_TEST) gdb -q -x ./gdb_scripts/make_cfg.py ./bin