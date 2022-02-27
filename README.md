# CARES Center Inventory

This is an application to manage inventory in food pantries, specifically the CARES Center and Kent State University.

## Installation

The requirements can be installed by optionally creating a virtual environment, activating it, and then running

`pip install -r requirements.txt`

This command should install all of the necessary dependencies and given versions for running the application. Once this is done the application can be run using any ASGI web server of your choosing, but uvicorn is included in `requirements.txt` by default. The command to run the server with uvicorn is

`uvicorn main:app`

optinally with a `--reload` flag for hot reloading.

## Structure

### main.py

`main.py` includes the main source code for running the appication. This is where FastAPI is set up and the backend logic is written.

### database.py

`database.py` is where the setup is for the database. This is where the URL is set, engine is made, along with other general config.

### models.py

`models.py` is where the pydantic models are kept. These allow for FastAPI to perform data validation and return typed data.

### static

The `static` directory is where static files such as CSS, JavaScript, or images are stored.

### templates

The `templates` directory is where HTML temlpates are stored for the application to render them.