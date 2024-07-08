# Copyright (C) 2024 Jack Green (jackgreen.co)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# file: Makefile
# date: 2024-01-12
# lang: GNU Makefile
#
# Makefile for jackgreen.co

SHELL          := /bin/sh
PROJECT_ROOT   := $(shell git rev-parse --show-toplevel)
CAT            := $(shell command -v cat)
CP_R           := $(shell command -v cp) -R
DOCKER         := $(shell command -v docker)
DOCKER_COMPOSE := $(shell command -v docker) compose
MONGOSH        := $(shell command -v mongosh)
MKDIR_P        := $(shell command -v mkdir) -p
OPENSSL        := $(shell command -v openssl)
PYTHON         := $(shell command -v python)
RM_RF          := $(shell command -v rm) -rf
TAILWIND       := $(shell command -v tailwindcss)
TOUCH          := $(shell command -v touch)

DIR_SCRIPTS    := $(PROJECT_ROOT)/scripts
DIR_ASSETS     := $(PROJECT_ROOT)/assets
DIR_DIST       := $(PROJECT_ROOT)/jackgreen_co/core/static
DIR_BUILD	   := $(PROJECT_ROOT)/build
DIR_CERTS      := $(DIR_BUILD)/ssl

DOCKER_CONTEXT := $(shell echo "ctx-$$RANDOM$$RANDOM")

ifeq ($(BUILD_ENV),)
    ifneq ($(filter run-app,$(MAKECMDGOALS)),)
        BUILD_ENV := development
    endif
    ifneq ($(filter run run-full build build-initdb build-containers,$(MAKECMDGOALS)),)
        BUILD_ENV := staging
    endif
    ifneq ($(filter deploy teardown,$(MAKECMDGOALS)),)
        BUILD_ENV := production
    endif
endif

.DEFAULT_GOAL := build-full

.PHONY: help clean build-css build-js build-images build-favicons build-fonts build-initdb build-containers \
	create-ca build-cert-app build-cert-mongo build-cert-redis build-certs build-essential build-full build \
	run-app run-full run deploy teardown

# fn/help
#
# display makefile help
help:
	@printf "jackgreen.co makefile\n\
usage: make [target]\n\
\n\
environment variables:\n\
    SERVER           the server to deploy to (required by: deploy, teardown)\n\
    BUILD_ENV        the build environment (optional)\n\
\n\
targets:\n\
    clean            delete all files in the build and dist directories and create an empty manifest file\n\
    build-css        build the css files using tailwindcss\n\
    build-js         copy all js files to the dist directory\n\
    build-images     optimize and resize all images in the media/images directory\n\
    build-favicons   copy all favicons to the dist directory\n\
    build-fonts      copy all fonts to the dist directory\n\
    build-initdb     build the database import files\n\
    build-containers build the docker container\n\
    create-ca        generate a CA key and certificate\n\
    build-cert-app   generate ECC key and certificate for the python application\n\
    build-cert-mongo generate ECC key and certificate for mongo\n\
    build-cert-redis generate ECC key and certificate for redis\n\
    build-certs      generate certificates for internal services\n\
    build-essential  run all build tasks except for building the docker container and certificates\n\
    build-full       run all build tasks including building the docker container and certificates\n\
    build            alias for build-essential\n\
    run-app          run the flask app in app-only mode\n\
    run-full         run the flask app in full mode\n\
    run              alias for run-app\n\
    deploy           deploy the app to the production server\n\
    teardown         stop and remove all containers on the production server\n"

# fn/clean
#
# delete all files in the dist directory and create an empty manifest filed named manifest.txt
clean:
	@$(RM_RF) $(DIR_BUILD)
	@$(RM_RF) $(DIR_DIST)/*
	@$(TOUCH) $(DIR_DIST)/manifest.txt

# fn/build-css
#
# build the css files using tailwindcss, rename the output file to include the md5 hash of the file
# and append the file name and hash to the manifest.txt file
build-css:
	@echo "info: building css"
	@$(MKDIR_P) $(DIR_DIST)/css
	@shopt -s nullglob; for file in $(DIR_ASSETS)/css/*; do \
		filename=$$(basename $$file); \
		filehash=$$(sha1sum $$file | awk '{print $$1}'); \
		echo "css/$$filename:css/$$filehash.css" >> $(DIR_DIST)/manifest.txt; \
		$(TAILWIND) -i $$file -o $(DIR_DIST)/css/$$filehash.css --minify >/dev/null 2>&1; \
	done

# fn/build-js
# 
# copy all js files to the dist directory, rename the output file to include the md5 hash of the file
# and append the file name and hash to the manifest.txt file
build-js:
	@echo "info: building js"
	@$(MKDIR_P) $(DIR_DIST)/js
	@shopt -s nullglob; for file in $(DIR_ASSETS)/js/*; do \
		filename=$$(basename $$file); \
		filehash=$$(sha1sum $$file | awk '{print $$1}'); \
		echo "js/$$filename:js/$$filehash.js" >> $(DIR_DIST)/manifest.txt; \
		$(CP_R) $$file $(DIR_DIST)/js/$$filehash.js; \
	done

# fn/build-images
#
# optimize and resize all images in the media/images directory and copy them to the dist directory
build-images:
	@echo "info: building images"
	@$(MKDIR_P) $(DIR_DIST)/media/images
	@shopt -s nullglob; for file in $(DIR_ASSETS)/media/images/*; do \
        $(DIR_SCRIPTS)/optimize-image.sh --verbose --input "$$file" --output $(DIR_DIST)/media/images; \
    done

# fn/build-favicons
#
# copy all favicons to the dist directory
build-favicons:
	@echo "info: building favicons"
	@$(MKDIR_P) $(DIR_DIST)/media/favicons
	@$(CP_R) $(DIR_ASSETS)/media/favicons/* $(DIR_DIST)/media/favicons

# fn/build-fonts
# 
# copy all fonts to the dist directory
build-fonts:
	@echo "info: building fonts"
	@$(MKDIR_P) $(DIR_DIST)/fonts
	@$(CP_R) $(DIR_ASSETS)/fonts/* $(DIR_DIST)/fonts

# fn/build-initdb
#
# build the database import files
build-initdb:
	@echo "info: building database import files"
	@$(MKDIR_P) $(DIR_BUILD)
	@BUILD_ENV=$(BUILD_ENV) $(PYTHON) $(DIR_SCRIPTS)/initdb/blog.py --input $(PROJECT_ROOT)/blog-posts --output $(DIR_BUILD)
	@BUILD_ENV=$(BUILD_ENV) $(PYTHON) $(DIR_SCRIPTS)/initdb/captcha.py --input $(PROJECT_ROOT)/captcha-data --output $(DIR_BUILD)
	@if [ $(BUILD_ENV) = "development" ]; then \
		echo "info: importing database"; \
		$(MONGOSH) --host 127.0.0.1 --port 27017 --quiet jackgreen_co $(DIR_BUILD)/initdb.js; \
	fi

# fn/build-container
#
# build the docker container
build-containers:
	@echo "info: building docker containers"
	@BUILD_ENV=$(BUILD_ENV) $(DOCKER_COMPOSE) build

# fn/create-ca
#
# generate a CA key and certificate
create-ca:
	@$(MKDIR_P) $(DIR_CERTS)
	@if [ ! -f $(DIR_CERTS)/ca.pem ]; then \
		echo "info: generating ECC CA key and certificate"; \
		$(OPENSSL) ecparam -genkey -name secp384r1 -out $(DIR_CERTS)/ca.key >/dev/null 2>&1; \
		$(OPENSSL) req -new -x509 -days 1825 -key $(DIR_CERTS)/ca.key \
		-subj "/C=UK/ST=London/L=London/O=jackgreen.co/OU=CA/CN=jackgreen.co CA" \
		-out $(DIR_CERTS)/ca.pem >/dev/null 2>&1; \
	fi

# fn/build-cert-app
#
# generate ECC key and certificate for the python application
build-cert-app: create-ca
	@$(MKDIR_P) $(DIR_CERTS)
	@echo "info: generating ECC key and certificate for app"
	@$(OPENSSL) req -new -newkey ec -pkeyopt ec_paramgen_curve:secp384r1 -nodes \
		-subj "/C=UK/ST=London/L=London/O=jackgreen.co/OU=Internal/CN=app.internal" \
		-out $(DIR_CERTS)/app-csr.pem -keyout $(DIR_CERTS)/app-key.pem >/dev/null 2>&1
	@$(OPENSSL) x509 -req -days 365 -in $(DIR_CERTS)/app-csr.pem -CA $(DIR_CERTS)/ca.pem \
		-extfile <(printf "subjectAltName=DNS:app.internal,DNS:app") \
		-CAkey $(DIR_CERTS)/ca.key -CAcreateserial \
		-out $(DIR_CERTS)/app-cert.pem >/dev/null 2>&1
	@$(CAT) $(DIR_CERTS)/app-key.pem $(DIR_CERTS)/app-cert.pem > $(DIR_CERTS)/app.pem

# fn/build-cert-mongo
#
# generate ECC key and certificate for mongo
build-cert-mongo: create-ca
	@$(MKDIR_P) $(DIR_CERTS)
	@echo "info: generating ECC key and certificate for mongo"
	@$(OPENSSL) req -new -newkey ec -pkeyopt ec_paramgen_curve:secp384r1 -nodes \
		-subj "/C=UK/ST=London/L=London/O=jackgreen.co/OU=Internal/CN=mongo.internal" \
		-out $(DIR_CERTS)/mongo-csr.pem -keyout $(DIR_CERTS)/mongo-key.pem >/dev/null 2>&1
	@$(OPENSSL) x509 -req -days 365 -in $(DIR_CERTS)/mongo-csr.pem -CA $(DIR_CERTS)/ca.pem \
		-extfile <(printf "subjectAltName=DNS:mongo.internal,DNS:mongo") \
		-CAkey $(DIR_CERTS)/ca.key -CAcreateserial \
		-out $(DIR_CERTS)/mongo-cert.pem >/dev/null 2>&1
	@$(CAT) $(DIR_CERTS)/mongo-key.pem $(DIR_CERTS)/mongo-cert.pem > $(DIR_CERTS)/mongo.pem

# fn/build-cert-redis
#
# generate ECC key and certificate for redis
build-cert-redis: create-ca
	@$(MKDIR_P) $(DIR_CERTS)
	@echo "info: generating ECC key and certificate for redis"
	@$(OPENSSL) req -new -newkey ec -pkeyopt ec_paramgen_curve:secp384r1 -nodes \
		-subj "/C=UK/ST=London/L=London/O=jackgreen.co/OU=Internal/CN=redis.internal" \
		-out $(DIR_CERTS)/redis-csr.pem -keyout $(DIR_CERTS)/redis-key.pem >/dev/null 2>&1
	@$(OPENSSL) x509 -req -days 365 -in $(DIR_CERTS)/redis-csr.pem -CA $(DIR_CERTS)/ca.pem \
		-extfile <(printf "subjectAltName=DNS:redis.internal,DNS:redis") \
		-CAkey $(DIR_CERTS)/ca.key -CAcreateserial \
		-out $(DIR_CERTS)/redis-cert.pem >/dev/null 2>&1
	@$(CAT) $(DIR_CERTS)/redis-key.pem $(DIR_CERTS)/redis-cert.pem > $(DIR_CERTS)/redis.pem

# fn/build-certs
#
# generate certificates for internal services
build-certs: build-cert-app build-cert-mongo build-cert-redis

# fn/build-essential
#
# run all build tasks except for building the docker container and certificates
build-essential: clean build-css build-js build-images build-favicons build-fonts build-initdb

# fn/build-full
#
# run all build tasks including building the docker container and certificates
build-full: build-essential build-certs build-containers

# fn/build
#
# alias for build-essential
build: build-essential

# fn/run-app
#
# run the flask app in app-only mode
run-app: build-essential
	@echo "info: running in app-only mode"
	@BUILD_ENV=$(BUILD_ENV) $(PYTHON) $(PROJECT_ROOT)/wsgi.py

# fn/run-full
#
# run the flask app in full mode
run-full: build-full
	@echo "info: running in full mode (build-env: $(BUILD_ENV))"
	@trap 'BUILD_ENV=$(BUILD_ENV) $(DOCKER_COMPOSE) down --volumes; exit 0' EXIT; \
		BUILD_ENV=$(BUILD_ENV) $(DOCKER_COMPOSE) up

# fn/run
#
# alias for run-full
run: run-full

# fn/deploy
#
# deploy the app to the production server
deploy: build-full
	@if test -z "$(SERVER)"; then \
		echo "error: SERVER is not set"; \
		exit 1; \
	fi
	@echo "WARNING: you are about to deploy to the production server."
	@read -p "are you sure you want to continue? [y/N] " confirm && [[ $$confirm == [yY] || $$confirm == [yY][eE][sS] ]] || (echo "deploy aborted." && exit 1)
	@echo "info: deploying to production"
	@$(DOCKER) context create $(DOCKER_CONTEXT) --docker "host=ssh://$(SERVER)" >/dev/null 2>&1
	@$(DOCKER) context use $(DOCKER_CONTEXT) >/dev/null 2>&1
	@BUILD_ENV=$(BUILD_ENV) $(DOCKER_COMPOSE) -f $(PROJECT_ROOT)/docker-compose.yml down
	@BUILD_ENV=$(BUILD_ENV) $(DOCKER_COMPOSE) -f $(PROJECT_ROOT)/docker-compose.yml up -d
	@$(DOCKER) context use default >/dev/null 2>&1
	@$(DOCKER) context rm $(DOCKER_CONTEXT) >/dev/null 2>&1

# fn/teardown
#
# stop and remove all containers on the production server
teardown:
	@if test -z "$(SERVER)"; then \
		echo "error: SERVER is not set"; \
		exit 1; \
	fi
	@echo "WARNING: you are about to take down the production server."
	@read -p "are you sure you want to continue? [y/N] " confirm && [[ $$confirm == [yY] || $$confirm == [yY][eE][sS] ]] || (echo "down aborted." && exit 1)
	@echo "info: taking down production server"
	@$(DOCKER) context create $(DOCKER_CONTEXT) --docker "host=ssh://$(SERVER)" >/dev/null 2>&1
	@$(DOCKER) context use $(DOCKER_CONTEXT) >/dev/null 2>&1
	@BUILD_ENV=$(BUILD_ENV) $(DOCKER_COMPOSE) -f $(PROJECT_ROOT)/docker-compose.yml down --volumes
	@$(DOCKER) context use default >/dev/null 2>&1
	@$(DOCKER) context rm $(DOCKER_CONTEXT) >/dev/null 2>&1
