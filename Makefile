.PHONY: all help translate test clean update compass collect rebuild

SETTINGS={{ project_name }}.settings
TEST_SETTINGS={{ project_name }}.test_settings

# target: help - display this message
help:
	@egrep "^# target:" [Mm]akefile

# target: fmt - run pre-commit checks
fmt:
	pre-commit run -a

# target: upd - install deps
upd:
	pip install -r requirements/local.txt

# target: mm - makemigrations
mm:
	python manage.py makemigrations

# target: mg - migrate
mg:
	python manage.py migrate

# target: run - run server
run:
	python manage.py runserver 0.0.0.0:8000
