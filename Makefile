PROJECT_PACKAGE := main
PROJECT_CONFIGURATION_PACKAGE := project
DJANGO_SETTINGS_MODULE := $(PROJECT_CONFIGURATION_PACKAGE).settings.dev


## Setup and initialize the project for development.
init:
	@printf "${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Environment settings${RESET}\n\n"

	rsync --ignore-existing .env.json.example .env.json

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Python dependencies${RESET}\n\n"

	poetry env use 3.8
	poetry install

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Node.js dependencies${RESET}\n\n"

	npm install

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Initial assets build${RESET}\n\n"

	npm run gulp -- build

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Database${RESET}\n\n"

	poetry run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Admin user${RESET}\n\n"

	poetry run python manage.py shell -c "from django.contrib.auth.models import User ; u = User.objects.filter(username='admin').first() ; print(u.username if u else '', end='')"|grep -w 'admin' || poetry run python manage.py createsuperuser --noinput --email=admin@example.com --username=admin 2>/dev/null

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Fixtures${RESET}\n\n"

	poetry run python manage.py loaddata project/fixtures/*

	@printf "\n\n${YELLOW}---------------- Done.${RESET}\n\n"


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
	poetry run python manage.py shell --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: s server
## Alias of "server".
s: server
## Launch a development server.
server:
	poetry run python manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS_MODULE)

## Generate new database migrations.
migrations:
	poetry run python manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODULE) ${ARG}

.PHONY: migrate
## Run the database migrations.
migrate:
	poetry run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: superuser
## Create a superuser.
superuser:
	poetry run python manage.py createsuperuser --settings=$(DJANGO_SETTINGS_MODULE)


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
	poetry run flake8

.PHONY: isort
## Check Python imports sorting.
isort:
	poetry run isort --check-only --recursive --diff $(PROJECT_PACKAGE) $(PROJECT_CONFIGURATION_PACKAGE)


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
