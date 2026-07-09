MAKEFLAGS += -j4


i: install
install: django-install frontend-install

### cleans up the build artifacts and virtual environment
.PHONY: clean clean-venv clean-frontend-build clean-frontend-node-modules
clean: clean-frontend-build clean-venv clean-frontend-node-modules

clean-venv:
	rm -r .venv

clean-frontend-build:
	cd frontend && rm -r ./dist

clean-frontend-node-modules:
	cd frontend && rm -r node_modules

### installs the virtual environment and dependencies
django-install:
	uv sync --locked

django-dev:
	DEBUG=true uv run python manage.py runserver 0.0.0.0:8000

.PHONY: vite-dev
vite-dev:
	cd frontend && pnpm run dev

frontend-install:
	cd frontend && pnpm install

vite-build:
	cd frontend && pnpm run build

makemigrations make migrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --no-input --clear

createcachetable cache:
	uv run python manage.py createcachetable --database cache

#! dev super user
dev-createsuperuser:
	docker compose -f dev/docker-compose.dev.yml exec app env DJANGO_SUPERUSER_PASSWORD=admin uv run python manage.py createsuperuser --noinput --username admin --email admin@example.com

prod-start:
	env ENVIRONMENT=production uv run granian \
		--interface asginl \
		--workers 3 \
 		--runtime-mode mt \
		--host 0.0.0.0 \
 		--port 8000 \
 		config.asgi:application

#### DOCKER DEV #### -----------------------------------------------------------------------------
.PHONY: dev-up dev
dev-up dev:
	docker compose -f dev/docker-compose.dev.yml up --build -d

.PHONY: dev-down dev-stop
dev-down dev-stop stop:
	docker compose -f dev/docker-compose.dev.yml down

.PHONY: dev-clean
dev-clean:
	docker compose -f dev/docker-compose.dev.yml down -v

.PHONY: dev-restart restart
dev-restart restart:
	make dev-down
	make dev-up

.PHONY: dev-logs
dev-logs logs:
	docker compose -f dev/docker-compose.dev.yml logs -f

.PHONY: dev-ps
dev-ps ps:
	docker compose -f dev/docker-compose.dev.yml ps

.PHONY: dev-bash bash
dev-bash bash:
	docker compose -f dev/docker-compose.dev.yml exec app bash

.PHONY: dev-shell shell
dev-shell shell:
	docker compose -f dev/docker-compose.dev.yml exec app uv run python manage.py shell -v 2

## - END DOCKER DEV - ## -------------------------------------------------------------------------
