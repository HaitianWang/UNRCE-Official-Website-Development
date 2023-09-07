## Running:
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

## Tests:
### Commands
- Run all tests: `./manage.py test`
- Run a specific test group: `./manage.py test tests/test_`**group**`.py`

| Useful flags | What they do |
|--------------|--------------|
| --keepdb     | Retains the database after testing is complete |
| --no-input   | Ignores prompt to keep copy of test db if tests fail |
| --failfast|Stops testing immediately if any test fails|
[Other Flags](https://docs.djangoproject.com/en/4.2/ref/django-admin/#test)

### Selenium tests:
All Selenium tests require that you have the matching browser with a Selenium extention installed for use in running the test.



### Writing tests:
All the test classes we write and use are subclasses of Django's test classes, which are themselves subclasses of Python's Unittest classes.
