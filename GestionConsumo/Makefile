default: run

run:
	python manage.py runserver

reload_tables:
	python manage.py makemigrations
	python manage.py migrate

delete_data:
	python manage.py flush

# Previamente hay que montar el entorno virtual
montar_django:
	pip install django==2.2.7
