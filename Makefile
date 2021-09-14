SHELL:=/bin/bash

.PHONY: storage
storage:
	@docker-compose \
		--file docker-compose.storage.yaml \
		up --detach

.PHONY: debezium
debezium:
	@docker-compose \
		--file docker-compose.debezium.yaml \
		up --detach

.PHONY: connect
connect:
	@docker-compose \
		--file docker-compose.connect.yaml \
		up --detach

.PHONY: all
all: storage debezium connect

.PHONY: stop
stop:
	docker-compose \
		--file docker-compose.storage.yaml \
		--file docker-compose.debezium.yaml \
		--file docker-compose.connect.yaml \
		stop
