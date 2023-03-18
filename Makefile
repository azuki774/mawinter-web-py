SHELL=/bin/bash
VERSION=latest
container_name=mawinter-web-py
.PHONY: build
build:
	docker build -t $(container_name):$(VERSION) -f build/Dockerfile .

run:
	# for devcontainer
	gunicorn flaskapp:app --config src/gunicorn.py 
