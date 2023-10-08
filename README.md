## Running:
1. `git clone "https://github.com/HaitianWang/UNRCE-Database-project"`
2. `cd UNRCE-django`
3. `python -m pip install --user virtualenv`
4. `python -m venv env`
5. Mac: `source env/bin/activate`, Windows: `.\env\Scripts\activate`
6. `pip install -r requirements.txt`
7. `python manage.py runserver`

## Tests:
### Commands
- Run all tests: `python manage.py test`
- Run a specific test group: `python manage.py test tests/test_`**group**`.py`

| Useful flags | What they do |
|--------------|--------------|
| --keepdb     | Retains the database after testing is complete |
| --no-input   | Ignores prompt to keep copy of test db if tests fail |
| --failfast|Stops testing immediately if any test fails|
| --parallel|Allows tests to run simultaneously|
[Other Flags](https://docs.djangoproject.com/en/4.2/ref/django-admin/#test)

### Selenium tests:
All Selenium tests require that you have the matching browser with a Selenium extention installed for use in running the test.



### Writing tests:
All the test classes we write and use are subclasses of Django's test classes, which are based on Python's Unittest module. 
### Including
`from django.test include SimpleTestCase, TransactionTestCase, TestCase`
`from django.contrib.staticfiles.testing import StaticLiveServerTestCase`
Best practice is to not include classes you won't use.


|Testing Class|What to use it for|
|---|---|
|SimpleTestCase|Tests that don't involve the database|
|TransactionTestCase|Testing if database transactions are working properly (unlikely to be used)|
|TestCase|Runs tests on a testing database that is cleaned up at the end|
|StaticLiveServerTestCase|Starts a live version of the server for testing, useful for Selenium tests|