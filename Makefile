DC = docker compose
APP = docker_compose/app.yaml
APP_DEV = docker_compose/app.dev.yaml
KAFKA = docker_compose/kafka.yaml
MONGO = docker_compose/mongo.yaml
MONGO_EXPRESS = docker_compose/mongo-express.yaml
APP_SERVICE = main-app

.PHONY: up-dev
up-dev:
	${DC} -f ${APP} -f ${APP_DEV} -f ${KAFKA} -f ${MONGO} -f ${MONGO_EXPRESS} up --build --abort-on-container-exit --attach ${APP_SERVICE} --no-log-prefix

.PHONY: shell
shell:
	${DC} -f ${APP} exec -it ${APP_SERVICE} bash

.PHONY: test
test:
	${DC} -f ${APP} exec ${APP_SERVICE} pytest
