# Manager Project

## Copy environment file and fill all requirements
    $ cp .env.template .env

## Run Server
- **Create Virtual environment**

    `$ python3 -m venv /path/to/new/virtual/environment`

  `$ source /path/to/new/virtual/environment/bin/activate`


- **Install dependencies**
    
    `$ pip install -r requirements.txt`

- **Run Migrations**

    `$  aerich init-db`

- **Run Server**

    `$ uvicorn --reload main:app --host 0.0.0.0 --port 5000`


