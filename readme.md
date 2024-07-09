# Personal Notes App


## Installation steps

### Manual

- create a projects folder
   
   ```mkdir projects```

- go to projects folder

- clone the repo

- Go to the project path

- Create a virtualenv 

    ```Python -m venv venv```

- Activate the virtualenv

    ```Source venv/Scripts/activate```

- Install the requirements

    ```pip install -r requirements.txt```

- Apply migrations

    ```python manage.py migrate```

- Start the server

    ```python manage.py runserver```

    - Server will start at 8000 port http://localhost:8000/

### Docker

- create a projects folder
   
   ```mkdir projects```

- go to projects folder

- clone the repo

- Go the the project path

- Start container

    ```docker-compose -f docker-compose.yml up -d```

- Stop container

    ```docker-compose -f docker-compose.yml down```