# ProyectoNoSQL

## For mongodb you must be inside MongoDB directory and then
python3 -m pip install virtualenv
python3 -m venv ./venv
.\venv\Scripts\Activate.ps1

### Install project python requirements
pip install -r requirements.txt

### Load data
docker run --name mongodb -d -p 27017:27017 mongo