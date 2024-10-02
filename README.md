# How to use the project

### 1. git clone https://github.com/kirilldarealcaucasian/cats_exhibition


### 2. Create .env file and add this
```yaml
  LOG_LEVEL=DEBUG
  DB_USER=postgres
  DB_PASSWORD=postgres
  DB_SERVER=db
  DB_PORT=5432
  DB_NAME=cats_db
```
### 3. cd project

### 4. docker compose up --build

### 5. When app has been started, you can go inside the container and run pytest ./tests/integration_tests/ to run tests

### Documentation is accessible at http://127.0.0.1:8000/docs#/