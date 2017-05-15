#!/bin/bash

# Activates virtualenv
. {{ django_env_path }}/bin/activate
export DJANGO_INSTALL_PATH={{ django_path }}
cd {{ django_project_path }}

# Updates the Whoosh index
python manage.py update_index
