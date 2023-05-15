# ersms-2023L
Train together - microservice architecture application for setting up community workouts

# Containerize Flask Application
https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-20-04

# Setup PostgreSQL database
Install PostgreSQL

(Linux)
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service
```
(macOS)
```bash
brew install postgresql@15
brew services start/stop postgresql@15
```

Setup database
```bash
psql postgres
```
```SQL
CREATE ROLE users_admin WITH LOGIN PASSWORD 'password';
ALTER ROLE chris CREATEDB;
```

Create necessary tables
```bash
flask db init
flask db migrate -m "users table"
flask db upgrade
```

Running the app requires environmental variables:
```bash
docker run -p 8080:8080 --env-file ./env.list woiro/ersms-api-gateway
```

env.list
```
SECRET_KEY=...
POSTGRES_DATABASE_URL=...
OAUTH_GOOGLE_CLIENT_ID=...
OAUTH_GOOGLE_CLIENT_SECRET=...
```