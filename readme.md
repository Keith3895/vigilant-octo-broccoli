# Identity Server

### Installation
1) Have python and all of python dependencies installed.
    1) [optional] install virualenv and setup a virtual environment to run the project.
2) Setup an postgreSQL instance.
    1) [To setup locally]. Use the commands/scripts in [./miscCMDs/init_pg_container.sh](./miscCMDs/init_pg_container.sh) file.
3) Install dependencies, run ``pip install -r requirements.txt``.

### Utilization
To run the application in development mode run the following:
1) set the env to be Dev: 
```
export FLASK_ENV=development
```
2) set the FLASK_APP value:
```
export FLASK_APP=identity_server
```
3) run the flask app.
```
flask run
```
