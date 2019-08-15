## Mongo DB

## Running the Database

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

## Database operations

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