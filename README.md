# User manager

A minimal web app for user managing developed with [Flask](http://flask.pocoo.org/) framework. 

#How to run 

- Step 1: Make shure you have Python and launched postgesql
- Step 2: Create virtual environment and activate
 ```bash
    python -m venv <venv name>
    source <venv name>/bin/activate
```
- Step 3: Install requirements 
 ```bash
    pip install -r requirements.txt
```
- Step 3: Configure SQLAlchemy DB URI 
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://<username>:<password>@localhost:5432/<databasename>'

```
- Step 4: Make migrations in current venv
```python
from app import db
db.create_all()

```
- Step 5: Run app
```bash
flask run
```

