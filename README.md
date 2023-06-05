# ersms-2023L
Train together - microservice architecture application for setting up community workouts

# Kubernetes locally - Minikube Deployment

Fill required secrets for pod deployment

secret.yaml
```
apiVersion: v1
kind: Secret
metadata:
  name: auth-secret
stringData:
  SECRET_KEY: ...
  OAUTH_GOOGLE_CLIENT_ID: ...
  OAUTH_GOOGLE_CLIENT_SECRET: ...
type: Opaque
```

```shell
minikube start
kubectl apply -f ./postgres_microservice/manifests/
kubectl apply -f ./api_gateway_microservice/manifests/
minikube service auth
```

# Archive

## Docker auth with local Postgres

### Containerize Flask Application
https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-20-04

### Setup PostgreSQL database locally
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
ALTER ROLE users_admin CREATEDB;
CREATE DATABASE users;
GRANT ALL PRIVILEGES ON DATABASE users TO users_admin;
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
POSTGRES_DATABASE_URL=postgresql://users_admin:password@host.docker.internal/users
OAUTH_GOOGLE_CLIENT_ID=...
OAUTH_GOOGLE_CLIENT_SECRET=...
```