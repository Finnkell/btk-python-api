## Clone REPO

```sh

~> git clone --branch master https://github.com/Finnkell/btk-python-api.git
~> cd btk-python-api
~> git checkout -b sprint-<fist_name_letter>0.1

```

# Whole project packages installation SET-UP

### First things first, create a ``venv`` or ``conda env`` to install the packages.

```sh

~> python -m venv btk_api_env
~> btk_api_env/Scripts/activate.bat
~> ./install_requirements.sh # it will install all packages necessary in the entire project

# BACKEND SET-UP and START SERVER
~> python ./backend/manage.py makemigrations && python ./backend/manage.py migrate 
~> python ./backend/manage.py createsuperuser
~> python ./backend/manage.py runserver

# FRONTEND START SERVER
~> streamlit run ./frontend/routes.py

```

## Installation SET-UP to Frontend only

```sh

~> cd ./frontend
~> python -m venv btk_api_front_env
~> btk_api_front_env/Scripts/activate.bat
~> pip install -r ./requirements.txt

```


## Installation SET-UP to Backend only

```sh

~> cd ./backend
~> python -m venv btk_api_back_env
~> btk_api_back_env/Scripts/activate.bat
~> pip install -r ./requirements.txt

```

### Backend Available Routes

```sh

# ADMIN
GET|POST localhost:<port>/admin

# SETUPS
GET|POST localhost:<port>/setups/svr_model/
GET|POST localhost:<port>/setups/svr_model/fit
GET|POST localhost:<port>/setups/svr_model/predict

# TOOLS
GET|POST localhost:<port>/tools/

# AUTH
POST localhost:<port>/auth/register/
POST localhost:<port>/auth/login

```