import API
import json


Steam = API.Steam()
Dota = API.Dota()

hero_list = []
user_list = []


def checkUserlist(sender):
    for user in getUsers():
        if sender == user['vk']:
            return user['steam32']
    return False


def connectUsers():
    global user_list
    with open('users.json') as u:
        user_list = json.load(u)
        u.close()


def delUser(vk):
    for user in user_list:
        if user['vk'] == vk:
            user_list.remove(user)


def addUser(vk, steam32):
    usr = {"vk": vk, "steam32": steam32}
    user_list.append(usr)


def getUsers():
    return user_list


def disconnectUsers():
    global user_list
    data = json.dumps(user_list)
    with open('users.json', 'w') as h:
        h.write(data)
        h.close()


def connectHeroes():
    global hero_list
    with open('heroes.json') as h:
        hero_list = json.load(h)
        h.close()


def getHeroes(hero_id):
    for hero in hero_list:
        if hero['id'] == hero_id:
            return hero['name']
    return 'Not Found'


def getAccount(steamid):

    """ Возвращает пользователя по Steam32 """

    steamid64 = int(steamid) + 76561197960265728
    players = Steam.getAccount(steamid64)['players']
    if players:
        for player in players:
            # print(f'Name: {player["personaname"]} '
            #       f'\nSteam32: {str(int(player["steamid"]) - 76561197960265728)} '
            #       f'\nSteam64: {player["steamid"]} '
            #       f'\nURL: {player["profileurl"]}')
            return player
    else:
        return False


def findAccount(steamlogin):

    """ Поиск пользователя по уникальной ссылке """

    player = Steam.findAccount(steamlogin)
    if player['success'] == 1:
        # print(f'Steam64: {player["steamid"]}')
        getAccount(int(player['steamid']) - 76561197960265728)
    elif player['success'] == 42:
        print('Не найдено')
    else:
        print(player)


def getMatchInfo(match_id, account_id=None):

    """ Возвращает информацию о матче, с аккаунтом возвращает информацию о конкретном персонаже """

    match = Dota.getMatchInfo(match_id)
    radiant_win = match['radiant_win']
    gm = match['game_mode']
    team = ['Radiant', 'Dire']
    try:
        if account_id:
            for player in match['players']:
                if player['account_id'] == account_id:
                    return [radiant_win, player, gm]
        else:
            for player in match['players']:
                if player['player_slot'] == 0:
                    print(team[0], radiant_win)
                elif player['player_slot'] == 128:
                    print(team[1], not radiant_win)
                heroname = getHeroes(player['hero_id'])
                aid = 'Anonymous'
                if player['account_id'] != 4294967295:
                    aid = player['account_id']
                print(f'\t[{aid}] - {heroname}[{player["level"]}] -'
                      # f'\tLH/DN: {player["last_hits"]}/{player["denies"]} '
                      f' GPM/XPM: {player["gold_per_min"]}/{player["xp_per_min"]} -'
                      f' Networth: {player["gold_spent"]} ')
    except KeyError:
        print(match)


def getHistory(account_id=None, hero_id=None, matches_requested=5):

    """ Возвращает историю матчей """

    matches = Dota.getHistory(account_id, hero_id, matches_requested)
    for match in matches['matches']:
        if account_id:
            for player in match['players']:
                if player['account_id'] == account_id:
                    player = getMatchInfo(match['match_id'], account_id)
                    win = True
                    kda = player[1]["kills"], player[1]["deaths"], player[1]["assists"]
                    if player[0] and player[1]['player_slot'] >= 128:
                        win = False
                    heroname = getHeroes(player[1]['hero_id'])
                    type = 'Error'
                    if player[2] == 22:
                        type = 'All Pick'
                    elif player[2] == 23:
                        type = 'Turbo'
                    else:
                        print(player[2])
                    print(f'{win} [{match["match_id"]}] [{type}] {heroname}[{player[1]["level"]}] {kda[0]}/{kda[1]}/{kda[2]}')
        else:
            print(match)

