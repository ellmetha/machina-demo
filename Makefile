PROJECT_PACKAGE := main
PROJECT_CONFIGURATION_PACKAGE := project
DJANGO_SETTINGS_MODULE := $(PROJECT_CONFIGURATION_PACKAGE).settings.dev

.PHONY: devserver shell migrate superuser qa lint isort


init:
	@echo ---------------- Initialization --- Environment settings
	@echo

	rsync --ignore-existing .env.json.example .env.json
	sed -i .bak "s/.*__whoami__.*/  \"DB_USER\": \"$USER\",/" .env.json
	rm -f .env.json.bak

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
	@echo ---------------- Done.


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to launch development server, generate
# locales, etc.
# --------------------------------------------------------------------------------------------------

c: console
console:
	pipenv run python manage.py shell --settings=$(DJANGO_SETTINGS_MODULE)

s: server
server:
	pipenv run python manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS_MODULE)

migrations:
	pipenv run python manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODULE) ${ARG}

migrate:
	pipenv run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

superuser:
	pipenv run python manage.py createsuperuser --settings=$(DJANGO_SETTINGS_MODULE)


# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

qa: lint isort

# Code quality checks (eg. flake8, etc).
lint:
	pipenv run flake8

# Import sort checks.
isort:
	pipenv run isort --check-only --recursive --diff $(PROJECT_PACKAGE) $(PROJECT_CONFIGURATION_PACKAGE)
