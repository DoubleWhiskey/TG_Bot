from random import choice, randint
from orm_database import all_players

users_list = all_players()


def kick_or_hug(action, player):
    victim = choice(list(filter(lambda x: x != player, users_list)))

    if action == 'kick':
        amount = randint(1, 32)
        impact = ('бьёт', 'выбивает')
        gift = ('зуб', 'зуба', 'зубов')

    else:
        amount = randint(1, 666)
        impact = ('обнимает', 'дарит')
        gift = ('цветочек', 'цветочка', 'цветочков')

    if amount % 10 == 1 and amount % 100 != 11:
        num = 0
    elif amount > 10 and amount % 10 in (2, 3, 4) and str(amount)[-2] != '1':
        num = 1
    else:
        num = 2

    return f"{player} {impact[0]} @{victim} и {impact[1]} {amount} {gift[num]}!"


