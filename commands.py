import API
import json


def connectConfig():
    with open("config.json", "r") as fconf:
        conf = json.load(fconf)
        fconf.close()
        return conf


Steam = API.Steam()
Dota = API.Dota()

hero_list = []
user_list = []
quests_list = {}

conf = connectConfig()
messages = conf['messages']
token = conf['keys']['vk_token']
group_id = conf['keys']['vk_group']

vk = API.VK(token, group_id)


def checkAll(sender, text, lenght, symbol, return_word):
    if checkLenght(text, lenght):
        if lenght == 1:
            return True
        for _lenght in range(lenght):
            if _lenght == 0:
                pass
            else:
                if checkSymbols(text[_lenght], symbol[_lenght-1]):
                    pass
                else:
                    if symbol == 1:
                        vk.sendMessage(sender, messages['check_errors']['need_numbers'])
                    elif symbol == 2:
                        vk.sendMessage(sender, messages['check_errors']['need_letters'])
                    return False
    else:
        return False
    return text[return_word]


def checkLenght(text, needlenght):
    if len(text) == needlenght:
        return True
    else:
        return False


def checkSymbols(text, type):
    if type == 1:
        if text.isdigit():
            return True
        else:
            return False
    elif type == 2:
        if text.isalpha():
            return True
        else:
            return False


def checkUserlist(sender):
    for user in user_list:
        if sender == user['vk']:
            return user['steam32']
    return False


def connectUsers():
    global user_list
    with open('users.json') as u:
        user_list = json.load(u)
        u.close()
    print('Пользователи загружены ' + str(len(getUsers())))

def delUser(vk):
    for user in user_list:
        if user['vk'] == vk:
            user_list.remove(user)


def addUser(vk, steam32):
    usr = {"vk": vk, "steam32": int(steam32), "balance": 0}
    user_list.append(usr)


def getUsers():
    return user_list


def disconnectUsers():
    global user_list
    data = json.dumps(user_list)
    with open('users.json', 'w') as h:
        h.write(data)
        h.close()
    print('Пользователи сохранены')

def disconnectQuests():
    global quests_list
    data = json.dumps(quests_list)
    with open('quests.json', 'w') as h:
        h.write(data)
        h.close()
    print('Квесты сохранены')

def connectQuests():
    global quests_list
    with open('quests.json') as h:
        quests_list = json.load(h)
        h.close()
    print('Квесты загружены')


def getQuests():
    return quests_list['quests']


def completeQuest(user, qid):
    quests_list['quests'][qid]['users_complete'].append(user)


def Quests(sender, qid=None, showcomplete=False):
        q = getQuests()
        response = ''
        if not qid:
            for quest in q:
                if showcomplete and sender in quest['users_complete']:
                    response += f'🏆 [{quest["id"]}] {quest["about"]}: {quest["reward"]}🔶\n'
                if not showcomplete and sender not in quest['users_complete']:
                    response += f'❌ [{quest["id"]}] {quest["about"]}: {quest["reward"]}🔶\n'
            if response:
                return response
        else:
            for quest in q:
                if quest['id'] == int(qid):
                    if sender in quest['users_complete']:
                        response = f'🏆 [{quest["id"]}] {quest["about"]}: {quest["reward"]}🔶\n'
                    if sender not in quest['users_complete']:
                        response = f'❌ [{quest["id"]}] {quest["about"]}: {quest["reward"]}🔶\n'
                    return response
        return ''



def connectHeroes():
    global hero_list
    with open('heroes.json') as h:
        hero_list = json.load(h)
        h.close()
    print('Герои загружены')


def getHeroes(hero_id=None, hero_name=None):
    if hero_id:
        for hero in hero_list:
            if hero['id'] == hero_id:
                return hero['name']
        return 'Not Found'
    elif hero_name:
        for hero in hero_list:
            if hero['name'] == hero_name:
                return hero['id']
        return False


def findAccountID(steamid):
    """ Возвращает пользователя по Steam32 """

    steamid64 = int(steamid) + 76561197960265728
    players = Steam.findAccountID(steamid64)['players']
    if players:
        for player in players:
            return player
    else:
        return False


def findAccountURL(steamlogin):
    """ Поиск пользователя по уникальной ссылке """

    player = Steam.findAccountURL(steamlogin)
    if player['success'] == 1:
        player = findAccountID(int(player['steamid']) - 76561197960265728)
        return player
    elif player['success'] == 42:
        return False
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
            response = ''
            for player in match['players']:
                if player['player_slot'] == 0:
                    if radiant_win:
                        response += '🏆 Radiant\n\n'
                    else:
                        response += '❌ Radiant\n\n'
                elif player['player_slot'] == 128:
                    if not radiant_win:
                        response += '\n🏆 Dire\n\n'
                    else:
                        response += '\n❌ Dire\n\n'
                heroname = getHeroes(player['hero_id'])
                aid = 'Anonymous'
                if player['account_id'] != 4294967295:
                    aid = player['account_id']
                response += (f'[{aid}] {heroname}[{player["level"]}]'
                             # f'\tLH/DN: {player["last_hits"]}/{player["denies"]}'
                             f' 📊 {player["kills"]}/{player["deaths"]}/{player["assists"]}'
                             f' 💰 {player["gold_spent"]}\n')
            return response
    except KeyError:
        print(match)


def getHistory(account_id=None, hero_id=None, json=False, matches_requested=5):
    """ Возвращает историю матчей """

    matches = Dota.getHistory(account_id, hero_id, matches_requested)
    response = ''
    if json:
        response = []
    if matches['status'] == 1:
        for match in matches['matches']:
            if account_id:
                for player in match['players']:
                    if player['account_id'] == account_id:
                        player = getMatchInfo(match['match_id'], account_id)
                        kda = player[1]['kills'], player[1]['deaths'], player[1]['assists']
                        win = False
                        # radiant-win # command radiant/dire
                        if player[0] and player[1]['player_slot'] <= 4:
                            win = True
                        if not player[0] and player[1]['player_slot'] >= 128:
                            win = True
                        heroname = getHeroes(player[1]['hero_id'])
                        type = 'Error'
                        if player[2] == 22:
                            type = 'All Pick'
                        elif player[2] == 23:
                            type = 'Turbo'
                        elif player[2] == 4:
                            type = 'Single Draft'
                        elif player[2] == 5:
                            type = 'All Random'
                        else:
                            print(player[2])
                        if win:
                            _win = '🏆'
                        else:
                            _win = '❌'
                        if not json:
                            response += f'{_win} [{match["match_id"]}] [{type}] {heroname}[{player[1]["level"]}] 📊 {kda[0]}/{kda[1]}/{kda[2]} 💰 {player[1]["gold_spent"]}\n'
                        else:
                            response.append([win, player[1]['hero_id'], [kda[0],kda[1],kda[2]]])
            else:
                print(match)
        return response
    else:
        return False
