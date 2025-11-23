up:
	docker compose up -d --build --force-recreate --renew-anon-volumes

down:
	docker compose down

logs:
	docker compose logs -f

.PHONY: up down logs
