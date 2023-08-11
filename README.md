# RoboDoc Project
Predicting diseases with artificial intelligence. 

TO GET THE SERVER STARTED:

delete the .db and all the 001initial.py files in common & register  /migrations directory if there is one before first time running

- you need to install all necessary packages, especially the django rest_framework with pip install djangorestframework
- go into gui/
- type python manage.py makemigrations
- type python manage.py migrate
- type python manage.py loaddata symptomlist.json
- type python manage.py runserver as below

~ To create an admin (to see userdatabase with 127.0.0.1/admin)
- type python manage.py createsuperuser
- enter email, username, password correctly, other information such as age, sex, usertype isnt necessary just type 1 or random value
- then you are ready, run the server and go to 127.0.0.1/admin and login as admin
  
  
  
START SERVER with: 
python manage.py runserver 
and call in browser:	http://127.0.0.1:8000/
to see website


DATABSE INTERFACE (not public): 
call in browser:  		http://127.0.0.1:8000/admin
Enter superuser username and password


MAKE SERVER AVAILIABLE IN LOCAL NETWORK: 
run server with:
python manage.py runserver 0.0.0.0:8000
get local IP Adress of your server-computer (e.g. ipconfig, ifconfig)
goto client-browser and enter: 
server-ip-adress:8000
  
# Directories

* [Apimedic Scraper](https://github.com/nothingnix/RoboDoc/tree/master/apimedic) - scripts to get disease data from  apimedic.com
* [Environment Setup](https://github.com/nothingnix/RoboDoc/tree/master/env)
