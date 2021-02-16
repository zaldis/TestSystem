# TestSystem

Simple system for test design

## HOW TO START

1. Run db via docker;
2. Provide .env file with system variables into `./myquestions.env`
3. Sync db: `./manage.py migrate`
4. Install python packages: `pip install -r requirements.txt`
5. Run server: `./manage.py runsslserver`

You also can start application via docker-compose:
Run command: `docker-compose up` from root folder.
