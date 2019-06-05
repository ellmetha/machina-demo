machina-demo
############

This project showcases a standard installation of django-machina_ without customization.

.. contents:: Table of Contents
    :local:

Requirements
============

Python_ 3.7+, Pipenv_ 3.5+, Django_ 2.2+.

Installation
============

You can install the project locally using the following commands:

.. code-block:: shell

  $ git clone https://github.com/ellmetha/machina-vanilla && cd machina-vanilla
  $ make init
  $ pipenv run python manage.py createsuperuser
  $ pipenv run python manage.py loaddata vanilla_project/fixtures*

*Alright!* Now all you have to do is to launch the development server using:

.. code-block:: shell

  $ make server

License
=======

MIT. See ``LICENSE`` for more details.

.. _Django: https://www.djangoproject.com
.. _django-machina: https://github.com/ellmetha/django-machina
.. _Pipenv: https://github.com/kennethreitz/pipenv
.. _Python: https://www.python.org
