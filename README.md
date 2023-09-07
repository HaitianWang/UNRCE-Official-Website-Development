To Run:
1. `git clone "https://github.com/HaitianWang/UNRCE-Database-project"`
2. `cd UNRCE-django`
3. `python -m pip install --user virtualenv`
4. `python -m venv env`
5. Mac: `source env/bin/activate`, Windows: `.\env\Scripts\activate`
6. `pip install -r requirements.txt`
7. `python3 manage.py runserver`

## To Run (Windows)
1. py -m pip install --user virtualenv
2. py -m venv env
3. .\env\Scripts\activate
4. Steps 4 and beyond see Mac

# Running tests:
./manage.py test 

| Useful flags | What they do |
|--------------|--------------|
| --keepdb     | Retains the database after testing is complete |
| --no-input   | Ignores prompt to keep copy of test db if tests fail |

