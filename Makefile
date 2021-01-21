
publish:
	./publish.sh

down:
	docker-compose down

rmvols:
	docker-compose down --volumes

dev:
	docker-compose down
	docker-compose -f docker-compose.yml up -d --build

tail:
	docker-compose logs -f

psql:
	docker exec -it llamalucky_db_1 psql -U postgres -d postgres

apishell:
	docker exec -it llamalucky_api_1 python
