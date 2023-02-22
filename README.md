# Manager Project

## Copy environment file and fill all requirements
    $ cp .env.template .env

## Run Server
- **Create Virtual environment**

    `$ python3 -m venv /path/to/new/virtual/environment`

  `$ source /path/to/new/virtual/environment/bin/activate`

- **To load fixture in database**

- **Install dependencies**
    
    `$ pip install -r requirements.txt`

- **Run Migrations**
      
    `$  aerich init -t core.database.TORTOISE_ORM`
    `$  aerich init-db`
    `$  aerich migrate`

- **Run Server**

    `$ uvicorn --reload core.main:app --host 0.0.0.0 --port 5000`


