# Tech documentation

A project to attempt to create a solid tool for documenting code internally for tech companies.

## Running the application

Both frontend and backend need to run simultaneously

#### Running the backend server

```bash
make backend
```

#### Running the frontend server

```bash
make frontend
```

#### Launching the Database

MongoDB is used. To install follow the steps [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/).

Using brew, all you need to do is run:
```bash
brew tap mongodb/brew
brew install mongodb-community@4.0
```

Then to run the database:

```bash
make db
```

To setup the database and insert data, run:

```bash
make db_setup
```

To see the documents in the document collection, run:

```bash
make db_show
```

To clean the database document collection, run:

```bash
make db_clean
```

To update the database for a specific repository manually instead of using the webhook, run:

```bash
make db_update repo_full_name=<fullname of repositories>
```

### Setting the webhook redirect

To set the webhook redirect to localhost:
```bash
make webhook
```

#### Check out the app

Visit http://localhost:8080/

## Development

### Saving python resources 

```bash
pip freeze > backend/requirements.txt
```

### Installing python resources

```bash
pip install -r backend/requirements.txt
```

### Clone the test folder locally

```bash
git clone git@github.com:codersdoc/Test.git
```

### Change the setup of the Github app

Go to this [link](https://github.com/settings/apps/tech-documentation).

### Useful links

* [Github enpoints available](https://developer.github.com/v3/apps/available-endpoints/).


## Miscallaneous 

### Tech and library used

* pyGithub
* mongo
* flask
* Vuejs
