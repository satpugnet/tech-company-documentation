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

#### Running the Database

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

#### Database operations

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
make db_update organisation_login=<organisation_login (i.e. codersdoc)> repo_full_name=<fullname of repositories (i.e. codersdoc/Test)>
```

### Setting the webhook redirect

To set the webhook redirecting to localhost, first install [smee](https://smee.io/)

```bash
npm install --global smee-client
```

Then, run

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

This folder is used to make some test on an organisation code.

```bash
git clone git@github.com:codersdoc/Test.git
```

### Test a request to the github api

```bash
curl -H "Authorization: token <token_value>" -H "Accept: application/vnd.github.machine-man-preview+json" https://api.github.com/user
```

## Github

### Change the setup of the Github app

Go to this [link](https://github.com/settings/apps/tech-documentation).

## Miscallaneous 

### Useful links

* [Github enpoints available](https://developer.github.com/v3/apps/available-endpoints/). 

### Tech and library used

* pyGithub
* mongo
* flask
* Vuejs
