from fabric import task
from invoke import Exit
import shlex
import textwrap

HOST = "ubuntu@44.253.6.177"
USER = "ubuntu"
PROJECT_DIR = "/var/www/shinecongo"
REPO_URL = "https://github.com/243gervais/shinecongo-web"
BRANCH = "main"

PYTHON_BIN = "python3"
VENV_DIR = f"{PROJECT_DIR}/venv"
VENV_PY = f"{VENV_DIR}/bin/python"
PIP_BIN = f"{VENV_DIR}/bin/pip"
ENV_FILE = f"{PROJECT_DIR}/.env"

DOMAIN = "shinecongo.com"
WWW_DOMAIN = "www.shinecongo.com"
DB_NAME = "shinecongo_db"
DB_USER = "shinecongo_user"
DB_PASSWORD_PLACEHOLDER = "CHANGE_ME"
STATIC_ROOT = f"{PROJECT_DIR}/staticfiles"

SERVICE_NAME = "gunicorn-shinecongo"
SOCKET_PATH = "/run/gunicorn-shinecongo/gunicorn.sock"

CERTBOT_EMAIL = "admin@shinecongo.com"

APP_USER = "ubuntu"
APP_GROUP = "www-data"


def _run(c, cmd, sudo=False):
    runner = c.sudo if sudo else c.run
    return runner(f"bash -lc {shlex.quote(cmd)}")


def _ensure_repo(c):
    _run(c, f"mkdir -p {PROJECT_DIR}", sudo=True)
    _run(c, f"chown -R {APP_USER}:{APP_GROUP} {PROJECT_DIR}", sudo=True)
    _run(c, f"if [ ! -d {PROJECT_DIR}/.git ]; then git clone {REPO_URL} {PROJECT_DIR}; fi")
    _run(c, f"cd {PROJECT_DIR} && git fetch --all")
    _run(c, f"cd {PROJECT_DIR} && git checkout {BRANCH}")
    _run(c, f"cd {PROJECT_DIR} && git pull origin {BRANCH}")


def _ensure_venv(c):
    _run(c, f"if [ ! -d {VENV_DIR} ]; then {PYTHON_BIN} -m venv {VENV_DIR}; fi")
    _run(c, f"{PIP_BIN} install --upgrade pip")
    _run(c, f"{PIP_BIN} install -r {PROJECT_DIR}/requirements.txt")


def _ensure_env_file(c):
    env_contents = textwrap.dedent(
        f"""\
        SECRET_KEY=CHANGE_ME
        DEBUG=False
        ALLOWED_HOSTS={DOMAIN},{WWW_DOMAIN}
        CSRF_TRUSTED_ORIGINS=https://{DOMAIN},https://{WWW_DOMAIN}
        DATABASE_URL=postgres://{DB_USER}:{DB_PASSWORD_PLACEHOLDER}@localhost:5432/{DB_NAME}

        EMAIL_HOST=
        EMAIL_PORT=587
        EMAIL_HOST_USER=
        EMAIL_HOST_PASSWORD=
        EMAIL_USE_TLS=True
        DEFAULT_FROM_EMAIL=noreply@shinecongo.com
        ADMIN_EMAIL=admin@shinecongo.com

        AWS_ACCESS_KEY_ID=
        AWS_SECRET_ACCESS_KEY=
        AWS_STORAGE_BUCKET_NAME=
        AWS_S3_REGION_NAME=
        AWS_S3_ENDPOINT_URL=
        AWS_S3_ADDRESSING_STYLE=path
        """
    ).strip()
    cmd = (
        f"if [ ! -f {ENV_FILE} ]; then cat <<EOF > {ENV_FILE}\n"
        f"{env_contents}\nEOF\nfi"
    )
    _run(c, cmd, sudo=True)
    _run(c, f"chown {APP_USER}:{APP_GROUP} {ENV_FILE}", sudo=True)
    _run(c, f"chmod 640 {ENV_FILE}", sudo=True)


def _ensure_postgres(c):
    # 1) Create role if missing (safe to run repeatedly)
    _run(
        c,
        (
            f"sudo -u postgres psql -tAc "
            f"\"SELECT 1 FROM pg_roles WHERE rolname='{DB_USER}'\" | grep -q 1 "
            f"|| sudo -u postgres psql -c "
            f"\"CREATE ROLE {DB_USER} LOGIN PASSWORD '{DB_PASSWORD_PLACEHOLDER}';\""
        ),
        sudo=True,
    )

    # 2) Create database if missing (must run outside DO blocks)
    _run(
        c,
        (
            f"sudo -u postgres psql -tAc "
            f"\"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'\" | grep -q 1 "
            f"|| sudo -u postgres createdb -O {DB_USER} {DB_NAME}"
        ),
        sudo=True,
    )



def _find_manage_py(c):
    result = _run(c, f"cd {PROJECT_DIR} && find . -maxdepth 4 -name manage.py -print -quit")
    manage_py = result.stdout.strip()
    if not manage_py:
        raise Exit("manage.py not found under project directory")
    return manage_py


def _get_wsgi_module(c, manage_py):
    cmd = (
        f"cd {PROJECT_DIR} && {PYTHON_BIN} - <<PY\n"
        "import re, pathlib\n"
        f"text = pathlib.Path('{manage_py}').read_text()\n"
        "m = re.search(r\"DJANGO_SETTINGS_MODULE[^'\"]*['\"]([^'\"]+)['\"]\", text)\n"
        "print(m.group(1) if m else '')\n"
        "PY"
    )
    result = _run(c, cmd)
    settings_module = result.stdout.strip()
    if not settings_module:
        raise Exit("Could not detect DJANGO_SETTINGS_MODULE in manage.py")
    if settings_module.endswith(".settings"):
        return settings_module.replace(".settings", ".wsgi")
    return f"{settings_module}.wsgi"


def _manage(c, manage_py, args):
    _run(c, f"cd {PROJECT_DIR} && {VENV_PY} {manage_py} {args}")


def _write_systemd_service(c, wsgi_module):
    service = textwrap.dedent(
        f"""\
        [Unit]
        Description=gunicorn-shinecongo
        After=network.target

        [Service]
        User=ubuntu
        Group=www-data
        WorkingDirectory=/var/www/shinecongo
        EnvironmentFile=/var/www/shinecongo/.env
        RuntimeDirectory=gunicorn-shinecongo
        RuntimeDirectoryMode=775
        ExecStartPre=/bin/rm -f /run/gunicorn-shinecongo/gunicorn.sock
        ExecStart=/var/www/shinecongo/venv/bin/gunicorn --access-logfile - --error-logfile - --workers 3 --bind unix:/run/gunicorn-shinecongo/gunicorn.sock <YOUR_WSGI_MODULE>:application
        Restart=always
        RestartSec=5

        [Install]
        WantedBy=multi-user.target
        """
    ).strip()
    cmd = f"cat <<EOF | sudo tee /etc/systemd/system/{SERVICE_NAME}.service > /dev/null\n{service}\nEOF"
    _run(c, cmd, sudo=True)


def _write_nginx_config(c):
    nginx_conf = textwrap.dedent(
        f"""\
        server {{
            server_name {DOMAIN} {WWW_DOMAIN};

            location /static/ {{
                alias {STATIC_ROOT}/;
                access_log off;
            }}

            location / {{
                include proxy_params;
                proxy_pass http://unix:{SOCKET_PATH}:;
                proxy_read_timeout 300;
                proxy_connect_timeout 300;
            }}

            add_header X-Frame-Options "SAMEORIGIN" always;
            add_header X-Content-Type-Options "nosniff" always;
            add_header Referrer-Policy "strict-origin-when-cross-origin" always;
            add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
            client_max_body_size 20M;
        }}
        """
    ).strip()
    cmd = (
        f"cat <<EOF | sudo tee /etc/nginx/sites-available/{DOMAIN} > /dev/null\n"
        f"{nginx_conf}\nEOF"
    )
    _run(c, cmd, sudo=True)
    _run(c, f"ln -sf /etc/nginx/sites-available/{DOMAIN} /etc/nginx/sites-enabled/{DOMAIN}", sudo=True)


def _ensure_packages(c):
    packages = (
        "python3-venv python3-pip nginx postgresql postgresql-contrib "
        "certbot python3-certbot-nginx git build-essential libpq-dev"
    )
    _run(c, "apt update", sudo=True)
    _run(c, f"apt install -y {packages}", sudo=True)


def _maybe_certbot(c):
    cert_path = f"/etc/letsencrypt/live/{DOMAIN}/fullchain.pem"
    result = _run(c, f"if [ -f {cert_path} ]; then echo yes; else echo no; fi", sudo=True)
    if result.stdout.strip() == "yes":
        return
    if not CERTBOT_EMAIL:
        print("Skipping certbot: set CERTBOT_EMAIL in fabfile.py")
        return
    _run(
        c,
        (
            "certbot --nginx --non-interactive --agree-tos "
            f"-m {CERTBOT_EMAIL} -d {DOMAIN} -d {WWW_DOMAIN}"
        ),
        sudo=True,
    )


@task
def bootstrap(c):
    _ensure_packages(c)
    _ensure_repo(c)
    _ensure_venv(c)
    _ensure_env_file(c)
    _ensure_postgres(c)

    manage_py = _find_manage_py(c)
    wsgi_module = _get_wsgi_module(c, manage_py)

    _manage(c, manage_py, "migrate")
    _manage(c, manage_py, "collectstatic --noinput")

    _write_systemd_service(c, wsgi_module)
    _write_nginx_config(c)

    _run(c, "systemctl daemon-reload", sudo=True)
    _run(c, f"systemctl enable --now {SERVICE_NAME}", sudo=True)
    _run(c, "nginx -t", sudo=True)
    _run(c, "systemctl reload nginx", sudo=True)

    _maybe_certbot(c)


@task
def deploy(c):
    _ensure_repo(c)
    _ensure_venv(c)

    manage_py = _find_manage_py(c)

    _manage(c, manage_py, "migrate")
    _manage(c, manage_py, "collectstatic --noinput")

    _run(c, f"systemctl restart {SERVICE_NAME}", sudo=True)
    _run(c, "nginx -t", sudo=True)
    _run(c, "systemctl reload nginx", sudo=True)


@task
def restart(c):
    _run(c, f"systemctl restart {SERVICE_NAME}", sudo=True)


@task
def logs(c):
    _run(c, f"journalctl -u {SERVICE_NAME} -f -n 200", sudo=True)


@task
def status(c):
    _run(c, f"systemctl status {SERVICE_NAME} --no-pager", sudo=True)
    _run(c, "nginx -t", sudo=True)
