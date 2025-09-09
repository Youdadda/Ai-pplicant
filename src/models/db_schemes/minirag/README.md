In order to get going with alembic migration tool you would need to :

### Alembic init:
1) Copy `alembic.ini.example` into an `alembic.ini` and change the `sqlalchemy.url` into the url of your database.

2) Make you're in the `src\models\db_schemes\minirag` and run:
```bash
$ alembic init alembic
```
3) Generate the migration file :
```bash
$ alembic revision --autogenerate -m "A meaningful meassage that describe the changes"
```
4) Execute the changes:
```bash
$ alembic upgrade head
```