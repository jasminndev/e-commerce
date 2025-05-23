mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
user:
	python3 manage.py createsuperuser
fix:
	python3 manage.py loaddata categories products regions attributes deliveries productimages