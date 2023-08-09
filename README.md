## About The Project
this is a booking service project


#### Built With:
  - python
  - django
  - drf
  - sqlite - postgresql
   ------------------------------------
#### Documentation:
    after running the server.
    find out the bellow path:
    http://127.0.0.1:8000/swagger/
#### Install locally
```bash
python -m venv env
source env/bin/activate
git clone git@github.com:fbluewhale/realtyna.git
cd realtyna
pip install -r requirements.txt
```

Migrate database and run project:
```
python manage.py migrate
python manage.py runserver

run tests:
```
python manage.py test
