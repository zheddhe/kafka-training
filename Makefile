SHELL := /bin/bash
.ONESHELL:
# flags de gestion du comportement sur erreur (sortie immediate et sur premiere erreur en pipe)
.SHELLFLAGS := -eu -o pipefail -c
# cible make par defaut : help
.DEFAULT_GOAL := help

REPLICAS ?= 3

up: ## Lance kafka avec REPLICA=? (entre 1 à 3) brokers
	docker-compose up --scale kafka=$(REPLICAS) -d

down: ## Arrête kafka
	docker-compose down

producer: ## Publie des messages en tant que producer
	python producer.py

consumer: ## Lit des messages en tant que consumer
	python consumer.py

delete: ## Supprime le topic test
	python admin.py delete --name test

create: ## Crée le topic test
	python admin.py create --name test --partition 2 --replication 3

recreate: ## Recrée le topic test
	python admin.py delete --name test
	python admin.py create --name test --partition 2 --replication 3

help: ## Affiche cette aide
	@awk 'BEGIN{FS=":.*##"; printf "\nTargets disponibles:\n\n"} /^[a-zA-Z0-9_.-]+:.*##/{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2} /^.DEFAULT_GOAL/{print ""} ' $(MAKEFILE_LIST)
