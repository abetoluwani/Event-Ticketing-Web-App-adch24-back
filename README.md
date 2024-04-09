# Event-Ticketing-Web-App-adch24-back
This directory contains the back-end code for the Event Ticketing Web App, built with FastAPI, a Python web framework. It handles data storage, user management, ticketing logic, and API endpoints for the front-end.

Technologies:

    FastAPI (Python)
    Database: PostgreSQL (recommended) - configure for your preferred database
    Prisma ORM

Prerequisites:

    Python 3.x installed


### Installation
Get started by doing the below:

1. Create a ```.env``` file and add the follow to it
    * DEFAULT_DATABASE
2. Run ```pip install -r requirements.txt``` to install project dependencies
3. After that, run the app using ```python3 -m app.main``` (assuming your cwd is not ```app```)