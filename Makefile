.PHONY: build push

IMAGE_TAG ?= $(shell git describe --tags --always)

build:
	docker build . -t mfreudenberg/arduino-builder:$(IMAGE_TAG)

push:
	@docker login -u ${DOCKER_USER} -p ${DOCKER_TOKEN}
	docker push mfreudenberg/arduino-builder:$(IMAGE_TAG)
