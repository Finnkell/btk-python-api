# WHOLE PROJECT PACKAGES INSTALLATION SET-UP

### First things first, create a ``venv`` or ``conda env`` to install the packages.

```sh

~> python -m venv btk_api_env
~> btk_api_env/Scripts/activate.bat
~> ./install_requirements.sh # it will install all packages necessary in the entire project

```

## INSTALLATION SET-UP to FrontEnd only

```sh

~> cd ./frontend
~> python -m venv btk_api_front_env
~> btk_api_front_env/Scripts/activate.bat
~> pip install -r ./requirements.txt

```


## INSTALLATION SET-UP to BackEnd only

```sh

~> cd ./backend
~> python -m venv btk_api_back_env
~> btk_api_back_env/Scripts/activate.bat
~> pip install -r ./requirements.txt

```