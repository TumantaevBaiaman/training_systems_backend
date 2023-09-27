# Training Systems
***
# Local development
## Initial requirements
Project uses `venv` for dependency management:
```shell
python3 -m venv venv
```

activate venv :
```shell
venv/bin/activate
```

requirements :
```shell
pip install -r requirements.txt
```

Copy and configure `.env` file.
```shell
cp .env.example .env
```

## Migrate

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

## Running Localhost

Run server:
```shell
python3 manage.py runserver
```