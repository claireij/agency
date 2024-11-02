# Agency API

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This project is a system to simplify and streamline the process of an executive producer.

### Installing Dependencies

1. **Python 3.10.4** - Follow the instructions to install the latest version of python for your project in the python docs (https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **PIP Dependencies** - Install the required dependencies by navigation to the root folder of your project and running:

```bash
pip3 install -r requirements.txt
```

### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up locally

1. Install Git and Postgres

2. Add your local database url in setup.sh, then run:
```bash
chmod +x setup.sh
source setup.sh
echo $DATABASE_URL
```

3. Install the python dependencies

```bash
pip install -r requirements.txt
```

4. Run the app

```bash
python3 app.py
```
### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Add the AUTH0_DOMAIN and the API_AUDIENCE in your .env file
6. Create new API permissions:
   - `get:movies`
   - `get:actors`
   - `delete:movies`
   - `delete:actors`
   - `post:movies`
   - `post:actors`
   - `patch:movies`
   - `patch:actors`
7. Create new roles for:
   - Casting Assistant
     - can `get:movies`, `get:actors` 
   - Casting Director:
     - can `get:movies`, `get:actors`, `delete:actors`, `patch:actors`, `patch:movies`, `post:actors`
   - Executive Producer
     - can perform all actions
8. Test your endpoints with the test_app.py file
   - Register 3 users - assign the Casting Assistant role to one, the Casting Director to another and Executive Producer role to the other.
   - Sign into each account and make note of the JWT.
   - Create and .env file and include all the JWT in the .env file. Naming the variable in the following manner:
        - CASTING_ASSISTANT
        - CASTING_DIRECTOR
        - EXECUTIVE_PRODUCER

   - Run the following commands:
        chmod +x setup.sh
        source setup.sh
   - Run the following command in your command line to test all the endpoints:

        ```bash
        python3 test_app.py
        ```


### Deployment Configuration

1. Download/Install the Heroku CLI

```bash
# Install, if Heroku as Standalone
curl https://cli-assets.heroku.com/install.sh | sh
# Or, use Homebrew on Mac
brew tap heroku/brew && brew install heroku
# Verify the installation
heroku --version
# Verify the download
which heroku
```

2. Log into Heroku with the following command

```bash
heroku login -i
```

3. Using requirements.txt to install dependencies

```bash
# Pip will read versions of all packages in the current environment and saves them to a text file.
pip freeze > requirements.txt
```

4. Procfile: There should be a Procfile with the following command in your project

```
web: gunicorn app:app
```

Gunicorn is a pure-Python HTTP server for WSGI applications.

5. Using runtime.txt: A runtime.txt specifies which exact Python version will be used. We are using python-3.9.13. 
Troubleshoot: Check if the version is supported by Heroku here: https://devcenter.heroku.com/articles/python-support#supported-runtimes
If not, change it.

### Deployment

1. Navigate in you project directory
2. If you haven't already, log into Heroku

```bash
heroku login -i
```

3. Before moving forward, make sure that your file structure matches to the below:

````
├── Procfile
├── app.py
├── manage.py
├── models.py
├── requirements.txt
├── runtime.txt
└── setup.sh
````

4. Run local migrations
    - Run the following commands
        ```bash
        # Ensure to have the postgres running locally
        pg_ctl -D /usr/local/var/postgres start
        # You need some dependencies installed to make manage.py work properly
        pip3 install -r requirements.txt
        # Set up the local environment variables
        chmod +x setup.sh
        source setup.sh
        ```

    - Check the current DATABASE_URL

        ```bash
        echo $DATABASE_URL
        # postgresql://postgres@localhost:5432/postgres
        ```

5. Database migration:
    - Include a manage.py file in your application

    - Include the following three new packages in requirements.txt or install them individually using:

        ```bash
        pip3 install Flask-Script==2.0.6
        pip3 install Flask-Migrate==2.7.0
        pip3 install psycopg2-binary==2.9.1
        ```
    - To migrate your local database to another database in the Heroku cloud, you will have to run these commands:

        ```bash
        python3 manage.py db init
        python3 manage.py db migrate -m "Initial migration"
        python3 manage.py db upgrade
        ```

6. Initialize Git

```bash
# Run it just once, in the beginning
git init
# For the first time commit, you need to configure the git username and email:
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

7. Create an App in Heroku Cloud
    - Run the following command:
        ```bash
        heroku create [my-app-name] --buildpack heroku/python
        # For example, 
        # heroku create myapp-663697908 --buildpack heroku/python
        # https://myapp-663697908.herokuapp.com/ | https://git.heroku.com/myapp-663697908.git
        ```

    - You can check that a remote repository was added to your git repository with the following terminal command:
        ```bash
        git remote -v
        ```

    - If you cannot see the Heroku "remote" repository URL in the output, you can use the command:
        ```bash
        git remote add heroku [heroku_remote_git_url]
        ```

8. Add PostgreSQL addon for our database

    ```bash
    heroku addons:create heroku-postgresql:hobby-dev --app [my-app-name]
    ```

9. Configure the App.
    - Run the following command
        ```bash
        heroku config --app [my-app-name]
        # DATABASE_URL:
        # postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1
        ```
    - Copy the DATABASE_URL generated from the step above and update your local enviroment variable:
        ```bash
        export DATABASE_URL="postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1"
        # Verify
        echo $DATABASE_URL
        # postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1
        ```

10. Push it!

    ```bash
    # Every time you make any edits to any file in the web_app folder
    # Check which files are ready to be committed
    git add -A
    git status
    git commit -m "your message"
    git push heroku main
    ```

11. Migrate the database

    ```bash
    heroku run python manage.py db upgrade --app [my-app-name]
    ```

### Endpoint Documentation

`GET '/api/v1.0/movies'`

- Fetches a dictionary of movies
- Request Arguments: None
- Returns: An object with one key, `movies`, that contains an array of objects with the keys `id`, `release_date` and `title`. 

```json
{
    "movies": [
        {
            "id": 55,
            "release_date": 1997,
            "title": "Titanic"
        }
    ]
}
```

`GET 'api/v1.0/actors'`

- Fetches a dictionary of actors
- Request Arguments: None
- Returns: An object with on key, `actors`, that contains an array of obejcts with the keys `age`, `gender`, `id` and `name`.

```json
{
    "actors": [
        {
            "age": 47,
            "gender": "male",
            "id": 54,
            "name": "Leonardo Di Caprio"
        },
    ]
}
```

`DELETE '/api/v1.0/movies/:id'`

- Deletes a movie based on the provided id in the URL
- Request Arguments: None
- Returns: An object with two keys, `deleted`and `success`, where the value of the `deleted` key is the id of the deleted movie.

```json
{
    "deleted": 55,
    "success": true
}
```

`DELETE '/api/v1.0/actors/:id'`

- Deletes an actor based on the provided id in the URL
- Request arguments: None
- Returns: An object with two keys, `deleted` and `success`, where the value of the `deleted` key is the id of the deleted actor.

```json
{
    "deleted": 54,
    "success": true
}
```

`POST '/api/v1.0/movies'`

- Creates a new movie
- Request arguments (all are mandatory):  
        {   
            "release_date": int,
            "title": string
        }
- Returns: An object with two keys, `success` and `movie`, that contains an object with the keys `id`, `release_date` and `title`.

```json
{
    "movie": {
        "id": 95,
        "release_date": 2002,
        "title": "8 Mile"
    },
    "success": true
}
```

`POST '/api/v1.0/actors'`

- Creates a new actor
- Request arguments (all are mandatory):
{
    "name": string,
    "age": int,
    "gender": string
}
- Returns: An object with two keys, `success` and `actor`, that contains an object with the keys `id`, `age`, `gender` and `name`.

```json
{
    "actor": {
        "age": 52,
        "gender": "male",
        "id": 99,
        "name": "Matthew McConaughey"
    },
    "success": true
}
```

`PATCH '/api/v1.0/movies/:id'`

- Updates an existing movie based on the provided id in the url
- Request arguments (needs to contain at least one of them):
    {   
        "release_date": int,
        "title": string
    }
- Returns: An object with two keys, `success` and `movie`, that contains an object with the keys `id`, `release_date` and `title`.

```json
{
    "movie": {
        "id": 57,
        "release_date": 1997,
        "title": "Titanic"
    },
    "success": true
}
```

`PATCH '/api/v1.0/actors/:id'`

- Updates an existing actor based on the provided in in the url
- Request arguments (needs to contain at least one of them):
    {
        "name": string,
        "age": int,
        "gender": string
    }
- Returns: An object with two keys, `success` and `actor`, that contains an object with the keys `id`, `age`, `gender` and `name`.

```json
{
    "actor": {
        "age": 52,
        "gender": "male",
        "id": 99,
        "name": "Matthew McConaughey"
    },
    "success": true
}
```
