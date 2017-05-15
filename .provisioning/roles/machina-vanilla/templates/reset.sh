#!/bin/bash

# Activates virtualenv
. {{ django_env_path }}/bin/activate
export DJANGO_INSTALL_PATH={{ django_path }}
cd {{ django_project_path }}

# Empty media files and delete the Whoosh index
rm -rf {{ django_path }}/media/*
rm -rf {{ django_path }}/.whoosh_index

# Resets the database and loads fixtures
python manage.py flush --noinput
python manage.py sqlsequencereset auth
python manage.py createsuperuser --username=admin --email=dev@machina-forum.io --noinput
python manage.py loaddata vanilla_project/fixtures/*

# Regenerates the Whoosh index
python manage.py update_index
