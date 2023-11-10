# Author: Dominik Harmim <harmim6@gmail.com>

DOC_DIR := docs
SRC_DIR := src
TESTS_DIR := $(SRC_DIR)/tests

DOCKER_NAME := kiwi-sorting
DOCKER_WORK_DIR := /usr/src/app
DOCKER := docker run --name $(DOCKER_NAME) --rm -v ./:$(DOCKER_WORK_DIR) \
	-p 5000:5000 -w $(DOCKER_WORK_DIR) $(DOCKER_NAME)


.PHONY: run
run: docker
	$(DOCKER) ./bootstrap.sh


.PHONY: tests
tests: docker
	$(DOCKER) pytest $(TESTS_DIR)


.PHONY: doc
doc: docker
	$(DOCKER) make -C $(DOC_DIR) html


.PHONY: docker
docker:
	docker build -t $(DOCKER_NAME) .
