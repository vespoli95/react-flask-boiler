# YUL-CODE

# Back-end (python, flask)

1. Install pip: https://pip.pypa.io/en/stable/installing/
2. Run: pip install pipenv
3. Run: pipenv install
4. Run: pipenv run shell
5. Run: py app.py
6. Navigate to: http://127.0.0.1:5000/

# setup local PostgreSQL database
1. Install pgAdmin
2. Create a database named 'GameTime'
3. Add a keys.py file to the root folder:
  ![keys.py](/documentation/keys_py_file.PNG)
4. Run: python
5. Run: from app import db
6. Run: db.create_all()
