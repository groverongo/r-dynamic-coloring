up:
	docker compose --env-file .env up -d --build --force-recreate --renew-anon-volumes

down:
	docker compose down

build:
	TAG=$(TAG) docker compose build $(services)
	@if [ "$(TAG)" != "latest" ] && [ ! -z "$(TAG)" ]; then \
		TAG=latest docker compose build $(services); \
	fi

push:
	TAG=$(TAG) docker compose push $(services)
	@if [ "$(TAG)" != "latest" ] && [ ! -z "$(TAG)" ]; then \
		TAG=latest docker compose push $(services); \
	fi

logs:
	docker compose logs -f

.PHONY: up down build push logs

load-envs:
	./scripts/load_envs.sh

platform-packages:
	cd packages/GraphCanvas && pnpm run build
	cd platform && rm pnpm-lock.yaml && rm -rf node_modules && pnpm install

platform-dev:
	cd platform && pnpm run dev

platform-build:
	cd platform && pnpm run build