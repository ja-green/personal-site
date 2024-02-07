# Copyright (C) 2024 Jack Green (jackgreen.co)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# file: Makefile
# date: 2024-01-12
# lang: GNU Makefile
#
# Makefile for jackgreen.co
# pass PRODUCTION=1 to build for production

SHELL         := /bin/sh
PROJECT_ROOT  := $(shell git rev-parse --show-toplevel)
MKDIR_P       := $(shell command -v mkdir) -p
RM_RF         := $(shell command -v rm) -rf
CP_R          := $(shell command -v cp) -R
TOUCH         := $(shell command -v touch)
PYTHON        := $(shell command -v python)
TAILWIND      := $(shell command -v tailwind)

DIR_SCRIPTS   := $(PROJECT_ROOT)/scripts
DIR_ASSETS    := $(PROJECT_ROOT)/assets
DIR_DIST      := $(PROJECT_ROOT)/jackgreen_co/core/static

.DEFAULT_GOAL := run

PRODUCTION    := 0
export PRODUCTION

ifeq ($(PRODUCTION), 1)
	TAILWIND_FLAGS := --minify
	WSGI_ENV       := production
else
	WSGI_ENV       := development
endif

.PHONY: run run-production build-css clean

# fn/clean
#
# delete all files in the dist directory and create an empty manifest filed named manifest.txt
clean:
	@$(RM_RF) $(DIR_DIST)/*
	@$(TOUCH) $(DIR_DIST)/manifest.txt

# fn/build-css
#
# build the css files using tailwindcss, rename the output file to include the md5 hash of the file
# and append the file name and hash to the manifest.txt file
build-css:
	@echo "building css"
	@$(MKDIR_P) $(DIR_DIST)/css
	@$(eval HASH := $(shell md5sum $(DIR_ASSETS)/css/main.css | awk '{print $$1}'))
	@echo "main.css:css/$(HASH).css" >> $(DIR_DIST)/manifest.txt
	@$(TAILWIND) -i $(DIR_ASSETS)/css/main.css -o $(DIR_DIST)/css/$(HASH).css $(TAILWIND_FLAGS) >/dev/null 2>&1

# fn/build-js
# 
# copy all js files to the dist directory, rename the output file to include the md5 hash of the file
# and append the file name and hash to the manifest.txt file
build-js:
	@echo "building js"
	@$(MKDIR_P) $(DIR_DIST)/js
	@$(eval HASH := $(shell md5sum $(DIR_ASSETS)/js/main.js | awk '{print $$1}'))
	@echo "main.js:js/$(HASH).js" >> $(DIR_DIST)/manifest.txt
	@$(CP_R) $(DIR_ASSETS)/js/main.js $(DIR_DIST)/js/$(HASH).js

# fn/build-images
#
# optimize and resize all images in the media/images directory and copy them to the dist directory
build-images:
	@echo "building images"
	@$(MKDIR_P) $(DIR_DIST)/media/images
	@shopt -s nullglob; for file in $(DIR_ASSETS)/media/images/*; do \
        $(DIR_SCRIPTS)/optimize-image.sh --verbose --input "$$file" --output $(DIR_DIST)/media/images; \
    done

# fn/build-favicons
#
# copy all favicons to the dist directory
build-favicons:
	@echo "building favicons"
	@$(MKDIR_P) $(DIR_DIST)/media/favicons
	@$(CP_R) $(DIR_ASSETS)/media/favicons/* $(DIR_DIST)/media/favicons

# fn/build-fonts
# 
# copy all fonts to the dist directory
build-fonts:
	@echo "building fonts"
	@$(MKDIR_P) $(DIR_DIST)/fonts
	@$(CP_R) $(DIR_ASSETS)/fonts/* $(DIR_DIST)/fonts

# fn/build
#
# run all build tasks
build: clean build-css build-js build-images build-favicons build-fonts

# fn/watch
#
# watch for changes to the assets directory and run the build task
watch:
	@find $(DIR_ASSETS) -type f | entr -c make build

# fn/run
#
# run the flask app
run: build
	@echo "running in $(WSGI_ENV) mode"
	@FLASK_ENV=$(WSGI_ENV) $(PYTHON) $(PROJECT_ROOT)/wsgi.py
