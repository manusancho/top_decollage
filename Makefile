#!make
#######################################################################
#Script Name	: Makefile                                                                                             
#Description	: Bernard-based Telegram bot build manager.
#Args         	: None
#Author       	: Manuel Sancho (manu.sancho at gmail.com)
#Version		: 0.0.1
#Date			: 22/06/2023
#######################################################################

include VERSION
export $(shell sed 's/=.*//' VERSION)

# include env file
include env/prod.env

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help dist push

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# COMMANDS
# Each entry represent a callable command.
#######################################################################
# Helper methods
#######################################################################
build: ## Build Docker image as "latest".
	docker build --file "./Dockerfile" --tag $(DOCKER_REGISTRY_URL):latest .

build-nc: ## Build Docker image as "latest" without caching.
	docker build --no-cache --file "./Dockerfile" --tag $(DOCKER_REGISTRY_URL):latest .

tag: ## Tag latest image as VERSION
	docker tag $(DOCKER_REGISTRY_URL):latest $(DOCKER_REGISTRY_URL):$(VERSION)

push: ## Push image to remote registry
	docker login $(DOCKER_REGISTRY_URL)
	docker push $(DOCKER_REGISTRY_URL):$(VERSION)

