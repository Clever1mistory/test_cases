from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from datetime import datetime

# Инициализация базы данных SQLite
db = SqliteExtDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    registered = DateTimeField()

class Transaction(BaseModel):
    id = IntegerField(primary_key=True)
    owner_id = ForeignKeyField(User, backref='transactions')
    direction = CharField(choices=['out', 'in'])
    amount = IntegerField()
    created = DateTimeField()

# Создание таблиц
db.create_tables([User, Transaction])

start_date = datetime(2023, 7, 5)
end_date = datetime(2023, 7, 20)

# Запрос к базе данных для получения списка пользователей с информацией о балансе и суммах транзакций
query = (User.select(User.id,User.name,fn.SUM(Case(None,[(Transaction.direction == 'in', Transaction.amount)],0)
             ).alias('in_sum'),
             fn.SUM(Case(None,[(Transaction.direction == 'out', Transaction.amount)],0)
             ).alias('out_sum'))
         .join(Transaction)
         .where(Transaction.created.between(start_date, end_date))
         .group_by(User.id))

# Вывод результатов запроса
for user in query:
    print(f"ID: {user.id}, Name: {user.name}, Balance: {user.in_sum - user.out_sum}, "
          f"Incoming Sum: {user.in_sum}, Outgoing Sum: {user.out_sum}")

# Закрытие соединения с базой данных
db.close()