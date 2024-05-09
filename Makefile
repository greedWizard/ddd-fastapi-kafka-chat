DC = docker compose
APP = docker_compose/app.yaml
APP_DEV = docker_compose/app.dev.yaml
KAFKA = docker_compose/kafka.yaml
MONGO = docker_compose/mongo.yaml
MONGO_EXPRESS = docker_compose/mongo-express.yaml
APP_SERVICE = main-app
ENV = --env-file .env

.PHONY: app-dev
app-dev:
	${DC} -f ${APP_DEV} -f ${KAFKA} ${ENV} up --build -d

.PHONY: app-dev-logs
app-dev-logs:
	${DC} -f ${APP_DEV} logs -f

.PHONY: storages
storages:
	${DC} -f ${MONGO} ${ENV} up -d --build

.PHONY: down-dev
down-dev:
	${DC} -f ${APP_DEV} -f ${KAFKA} ${ENV} down

.PHONY: down
down:
	${DC} -f ${APP} -f ${APP_DEV} -f ${KAFKA} -f ${MONGO} -f ${MONGO_EXPRESS} ${ENV} down

.PHONY: ui
ui:
	${DC} -f ${MONGO_EXPRESS} ${ENV} up --build -d

.PHONY: purge
purge:
	${DC} -f ${KAFKA} -f ${MONGO} -f ${MONGO_EXPRESS} ${ENV} down -v

.PHONY: shell
shell:
	${DC} -f ${APP} exec -it ${APP_SERVICE} bash

.PHONY: test
test:
	${DC} -f ${APP} exec ${APP_SERVICE} pytest
