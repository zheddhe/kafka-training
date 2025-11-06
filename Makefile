REPLICAS ?= 3

up:
	docker-compose up --scale kafka=$(REPLICAS) -d

down:
	docker-compose down

producer:
	python producer.py

consumer:
	python consumer.py

delete:
	python admin.py delete --name test

create:
	python admin.py create --name test --partition 2 --replication 3

recreate:
	python admin.py delete --name test
	python admin.py create --name test --partition 2 --replication 3