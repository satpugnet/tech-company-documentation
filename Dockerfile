FROM python:3.7

WORKDIR /usr/src

COPY backend /usr/src/backend
COPY frontend /usr/src/frontend

# Install backend dependencies
RUN pip install -r backend/requirements.txt

# Install YARN
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get -y update
RUN apt-get -y install yarn

# Install frontend dependencies
RUN yarn --cwd frontend install