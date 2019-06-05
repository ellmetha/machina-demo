PROJECT_PACKAGE := main
PROJECT_CONFIGURATION_PACKAGE := project
DJANGO_SETTINGS_MODULE := $(PROJECT_CONFIGURATION_PACKAGE).settings.dev


## Setup and initialize the project for development.
init:
	@echo ---------------- Initialization --- Environment settings
	@echo

	rsync --ignore-existing .env.json.example .env.json

	@echo
	@echo
	@echo ---------------- Initialization --- Python dependencies
	@echo

	pipenv install --dev

	@echo
	@echo
	@echo ---------------- Initialization --- Node.js dependencies
	@echo

	npm install

	@echo
	@echo
	@echo ---------------- Initialization --- Initial assets build
	@echo

	npm run gulp -- build

	@echo
	@echo
	@echo ---------------- Initialization --- Database
	@echo

	pipenv run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

	@echo
	@echo
	@echo ---------------- Initialization --- Admin user
	@echo

	pipenv run python manage.py shell -c "from django.contrib.auth.models import User ; u = User.objects.filter(username='admin').first() ; print(u.username if u else '', end='')"|grep -w 'admin' || pipenv run python manage.py createsuperuser --noinput --email=admin@example.com --username=admin 2>/dev/null

	@echo
	@echo
	@echo ---------------- Initialization --- Fixtures
	@echo

	pipenv run python manage.py loaddata project/fixtures/*

	@echo
	@echo ---------------- Done.


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to launch development server, generate
# locales, etc.
# --------------------------------------------------------------------------------------------------

.PHONY: c console
## Alias of "console".
c: console
## Launch a development console.
console:
	@echo does nothing
	pipenv run python manage.py shell --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: s server
## Alias of "server".
s: server
## Launch a development server.
server:
	pipenv run python manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS_MODULE)

## Generate new database migrations.
migrations:
	pipenv run python manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODULE) ${ARG}

.PHONY: migrate
## Run the database migrations.
migrate:
	pipenv run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: superuser
## Create a superuser.
superuser:
	pipenv run python manage.py createsuperuser --settings=$(DJANGO_SETTINGS_MODULE)


# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

.PHONY: qa
## Trigger all quality assurance checks.
qa: lint isort

.PHONY: lint
## Trigger code quality checks (flake8).
lint:
	pipenv run flake8

.PHONY: isort
## Check Python imports sorting.
isort:
	pipenv run isort --check-only --recursive --diff $(PROJECT_PACKAGE) $(PROJECT_CONFIGURATION_PACKAGE)


# MAKEFILE HELPERS
# ~~~~~~~~~~~~~~~~
# The following rules can be used to list available commands and to display help messages.
# --------------------------------------------------------------------------------------------------

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: help
## Print Makefile help.
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<action>${RESET}'
	@echo ''
	@echo 'Actions:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)-30s${RESET}\t${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -t'|' -sk1,1
