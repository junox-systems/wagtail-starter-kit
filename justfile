export SITE := "wagtail-starter-kit"
export DEV_ENV := "development"
export PROD_ENV := "production"
export VENV_PY := ".venv/bin/python"

# ---- PROD ---- #

prod-setup:
    just freebsd-nginx-configure
    just freebsd-wagtail-configure
    just freebsd-litestream-configure
    just setup-env
    just setup-pip
    just setup-pf

prod-post-setup:
    just setup-staticfiles
    just litestream-restore
    just setup-db
    just prod-start

freebsd-setup-pkgs:
    pkg install --yes git nginx litestream go-anubis just python311 py311-uvicorn py311-uvloop py311-pillow py311-pillow-heif py311-granian py311-sqlite3 py311-pip

freebsd-nginx-configure:
    # enable nginx
    sysrc nginx_enable=YES

    # remove nginx.conf
    rm /usr/local/etc/nginx/nginx.conf

    # create nginx.conf symlink from the repo
    ln -sf $(pwd)/prod/freebsd/nginx/nginx.conf \
            /usr/local/etc/nginx/nginx.conf

    # create conf.d directory
    install -d -m 0755 /usr/local/etc/nginx/conf.d

    # create wagtail.conf symlink from the repo
    ln -sf $(pwd)/prod/freebsd/nginx/wagtail.conf \
            /usr/local/etc/nginx/conf.d/wagtail.conf

    # start nginx
    service nginx restart || service nginx start

freebsd-litestream-configure:
    # enable litestream
    sysrc litestream_enable=YES
    sysrc litestream_config=/usr/local/etc/litestream.yml

    # ensure config exists (from repo)
    ln -sf $(pwd)/prod/freebsd/litestream/litestream.yml \
        /usr/local/etc/litestream.yml

    # install rc.d service from repo
    install -m 555 $(pwd)/prod/freebsd/rc.d/litestream \
        /usr/local/etc/rc.d/litestream

litestream-status:
    @echo "== service status =="
    service litestream status || true

    @echo "== process =="
    pgrep -fl litestream || true

    @echo "== socket / activity =="
    sockstat -4 | grep litestream || true

litestream-restore:
    @echo "== restore =="
    CMD="$(pwd)/prod/freebsd/scripts/litestream-restore.sh" \
        just run-www

litestream-backup:
    # load env
    . /usr/local/etc/wagtail/env && \
    echo "Starting replication..." && \
    litestream replicate

setup-env:
    # env file (secrets)
    awk 'NF && $1 !~ /^#/ {print "export " $0} !NF || $1 ~ /^#/ {print}' $(pwd)/.env.prod > /usr/local/etc/wagtail/env

    chmod 640 /usr/local/etc/wagtail/env
    chown root:www /usr/local/etc/wagtail/env

freebsd-wagtail-configure:
    # runtime + data dirs
    install -d -o www -g www -m 755 /var/db/wagtail
    install -d -o www -g www -m 755 /var/cache/nginx/wagtail

    # config dir (root-owned)
    install -d -m 755 /usr/local/etc/wagtail

    # ensure repo ownership for runtime user
    chown -R www:www /usr/local/www/wagtail

    # install rc.d service from repo
    install -m 555 $(pwd)/prod/freebsd/rc.d/wagtail \
        /usr/local/etc/rc.d/wagtail

    # enable service
    sysrc wagtail_enable=YES

mise-set-to-dev:
    sed -i 's/production/development/g' .miserc.toml

mise-set-to-prod:
    sed -i 's/development/production/g' .miserc.toml

setup-mise:
    # trust and install
    CMD="mise trust" just run-www
    CMD="mise install" just run-www

prepare-pip:
    uv lock
    uv pip compile pyproject.toml > requirements.txt
setup-pip:
    CMD="[ -d .venv ] || python3.11 -m venv --system-site-packages .venv && .venv/bin/pip install -r requirements.txt" just run-www

setup-uv:
    CMD="uv sync --locked --no-cache --no-dev" just run-www

setup-pf:
    # enable pf at boot
    sysrc pf_enable=YES

    # backup existing config (once)
    [ -f /etc/pf.conf ] && cp /etc/pf.conf /etc/pf.conf.bak || true

    # symlink repo pf.conf
    ln -sf $(pwd)/prod/freebsd/pf/pf.conf /etc/pf.conf

    # validate config BEFORE applying (critical)
    pfctl -nf /etc/pf.conf

    # load rules safely
    pfctl -f /etc/pf.conf

    # show active rules (sanity check)
    pfctl -sr

setup-cron:
    sh $(pwd)/prod/freebsd/scripts/setup-cron.sh

setup-staticfiles:
	CMD="$VENV_PY manage.py collectstatic --no-input --clear" just run-www

setup-db:
    just prod-migrate

prod-migrate:
	CMD="$VENV_PY manage.py migrate" just run-www

prod-start:
    service litestream restart || service litestream start
    service wagtail restart || service wagtail start
    service nginx reload

# helper function to run as www on server
run-www:
    env HOME=/home/www su -m www -c "sh -c '$CMD'"

git-pull:
	CMD="git pull --ff-only" just run-www

################################################################################
# ---- DEV ---- #
################################################################################

vite-install:
	cd frontend && pnpm install

django-install:
	uv sync

django-dev:
	DEBUG=true uv run granian --reload \
		--reload-ignore-paths /app/db/ \
		--interface asginl \
		--workers 2 \
		--runtime-mode mt \
		--log-level debug \
		--host 0.0.0.0 \
		--port 8000 \
		config.asgi:application

makemigrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

vite-dev:
	cd frontend && pnpm run dev

vite-build:
	cd frontend && pnpm run build

[parallel]
install: vite-install django-install

[parallel]
dev: django-dev vite-dev
