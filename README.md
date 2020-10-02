## Test coverage
```
coverage run manage.py test && coverage report --skip-covered
coverage html
```

## Docker compose

```
docker-compose up --build
````

### Add admin user
```
docker-compose exec django python3 /src/manage.py loaddata authentication_admin
```
