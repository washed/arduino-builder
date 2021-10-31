.PHONY: build push

IMAGE_TAG=${GA_TAG:-$(shell git describe --tags --always)}

build:
	docker build . -t mfreudenberg/arduino-builder:$(IMAGE_TAG)

push:
	@docker login -u ${DOCKER_USER} -p ${DOCKER_TOKEN}
	docker push .
