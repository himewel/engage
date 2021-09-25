SHELL:=/bin/bash

.PHONY: init
init:
	docker network create engage_network

.PHONY: storage
storage:
	docker-compose \
		--file docker-compose.storage.yaml \
		up --detach

.PHONY: debezium
debezium:
	docker-compose \
		--file docker-compose.debezium.yaml \
		up --detach

.PHONY: connect
streaming:
	docker-compose \
		--file docker-compose.streaming.yaml \
		up --detach

.PHONY: all
all: storage debezium streaming

.PHONY: stop
stop:
	docker-compose \
		--file docker-compose.storage.yaml \
		--file docker-compose.debezium.yaml \
		--file docker-compose.streaming.yaml \
		stop

.PHONY: reset
reset:
	docker-compose \
		--file docker-compose.storage.yaml \
		--file docker-compose.debezium.yaml \
		--file docker-compose.streaming.yaml \
		down --volumes --remove-orphans

.PHONY: build
build:
	docker-compose \
		--file docker-compose.storage.yaml \
		--file docker-compose.debezium.yaml \
		--file docker-compose.streaming.yaml \
		build
