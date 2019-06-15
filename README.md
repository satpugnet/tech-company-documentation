# Tech documentation

A project to attempt to create a solid tool for documenting code internally for tech companies.

## Running the application

Both frontend and backend need to run simultaneously

#### Running the backend server

```bash
pip install -r requirements.txt
cd backend/
python3 webserver.py
```

#### Running the frontend server

```bash
cd frontend/
yarn install
yarn run serve
```

#### Check out the app

Visit http://localhost:8081/

## Development

### Saving python resources 

```bash
pip freeze > requirements.txt
```

### Installing python resources

```bash
pip install -r requirements.txt
```

## Miscallaneous 

### Tech and library used

* pyGithub
