from random import choice, randint
from orm_database import all_players, Player

users_list = all_players()


def kick_or_hug(action, player):
    if not users_list or (len(users_list) == 1 and player in users_list):
        return f"Тут никого нет. Попробуй позвать друзей."
    victim = choice(list(filter(lambda x: x != player, users_list)))
    amount = randint(1, 32)
    player_in_db = Player.get(username=player)
    victim_in_db = Player.get(username=victim)
    if action == 'kick':
        impact = ('бьёт', 'выбивает')
        gift = ('зуб', 'зуба', 'зубов')
        player_in_db.combats += 1
        player_in_db.teeth += amount
        victim_in_db.kicks_get += 1

    else:
        impact = ('обнимает', 'дарит')
        gift = ('цветочек', 'цветочка', 'цветочков')
        player_in_db.hugs += 1
        player_in_db.flowers += amount
        victim_in_db.hugs_get += 1

    if amount % 10 == 1 and amount % 100 != 11:
        num = 0
    elif amount > 10 and amount % 10 in (2, 3, 4) and str(amount)[-2] != '1':
        num = 1
    else:
        num = 2
    player_in_db.save()
    victim_in_db.save()
    return f"{player} {impact[0]} @{victim} и {impact[1]} {amount} {gift[num]}!"


