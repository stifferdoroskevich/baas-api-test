## How to run project locally
```
FIRST
docker pull postgres:12
docker run -d -p 5444:5432 --name dbdock -e POSTGRES_PASSWORD=dockdock -d postgres:12

SECOND
git clone https://github.com/stifferdoroskevich/baas-api-test.git
cd desafio-dev-api-rest
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py init_db
python3 manage.py create_pessoas
python3 server.py
```

## API Documentation
bit.ly/documentacao_dock

## Verification of Data:
* URL: 127.0.0.1:5000/pessoas
* Should return 3 rows 
