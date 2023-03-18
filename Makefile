SHELL=/bin/bash
VERSION=latest
container_name=mawinter-web-py
.PHONY: build run
build:
	docker build -t $(container_name):$(VERSION) -f build/Dockerfile .

run:
	# for devcontainer
	cd src && gunicorn flaskapp:app --config gunicorn.py 
