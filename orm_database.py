from config import DATABASE_PATH
from peewee import *

conn = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = conn


class Player(BaseModel):
    player_id = AutoField(column_name='id')
    username = TextField(column_name='Username', default=None)
    combats = IntegerField(column_name='Combats', default=0)
    teeth = IntegerField(column_name='Teeth', default=0)
    hugs = IntegerField(column_name='Hugs', default=0)
    flowers = IntegerField(column_name='Flowers', default=0)
    kicks_get = IntegerField(column_name='Kicks_get', default=0)
    hugs_get = IntegerField(column_name='Hugs_get', default=0)

    class Meta:
        table_name = 'players'


def add_player(new_player):
    if new_player not in all_players():
        Player.create(username=new_player)


def del_player(pla):
    pl = Player.get(Player.username == pla)
    pl.delete_instance()


def statistic(_player):
    player_stats = Player.get(Player.username == _player)
    return f"""
Статистика {_player}:
ударов -> {player_stats.combats}
зубов выбито -> {player_stats.teeth}
прилётов в зубы -> {player_stats.kicks_get}

***________________***

обнимашек -> {player_stats.hugs}
цветов подарено -> {player_stats.flowers}
получил(а) объятий -> {player_stats.hugs_get}
"""


def all_players():
    players_list = [player.username for player in Player.select()]
    return players_list


conn.close()
