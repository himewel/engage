SHELL:=/bin/bash

.PHONY: init
init:
	@docker network inspect engage_network --format {{.Id}} 2>/dev/null \
		|| docker network create engage_network

.PHONY: storage
storage: init
	docker-compose \
		--file docker-compose.storage.yaml \
		up --detach

.PHONY: debezium
debezium: init
	docker-compose \
		--file docker-compose.debezium.yaml \
		up --detach

.PHONY: connect
streaming: init
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
	docker network rm engage_network

.PHONY: build
build:
	docker-compose \
		--file docker-compose.storage.yaml \
		--file docker-compose.debezium.yaml \
		--file docker-compose.streaming.yaml \
		build
	docker build ./profiler \
	 	--tag engage_profiler

.PHONY: profile
profile:
	docker run \
		--interactive \
		--name engage_profiler \
		--network engage_network \
		--tty \
		--rm \
		engage_profiler
