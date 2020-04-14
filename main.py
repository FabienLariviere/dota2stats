from commands import *


def getMessage():
    event = vk.getUpdate()
    if event['updates']:
        msg = vk.decodeUpdate(event)
        if msg and msg[1][0] == '/':
            sender, text = msg
            text = text.split(' ')
            return [sender, text]


def commandAdd():
    check = checkAll(sender, text, 2, [1], 1)
    if check:
        check = checkUserlist(sender)
        if not check:
            steam32 = findAccountID(text[1])
            if steam32:
                addUser(sender, text[1])
                vk.sendMessage(sender, messages['add']['success'])
            else:
                vk.sendMessage(sender, messages['add']['not_found'])
        else:
            vk.sendMessage(sender, messages['add']['error'])


def commandDel():
    if checkAll(sender, text, 1, None, None):
        check = checkUserlist(sender)
        if check:
            delUser(sender)
            vk.sendMessage(sender, messages['delete']['success'])
        else:
            vk.sendMessage(sender, messages['delete']['error'])

def commandFID():
    check = checkAll(sender, text, 2, [1], 1)
    if check:
        search = findAccountID(check)
        if search:
            response = f'Имя профиля: {search["personaname"]}\n' \
                       f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                       f'Steam64: {search["steamid"]}\n' \
                       f'URL: {search["profileurl"]}'
            vk.sendMessage(sender, messages['find']['success'] + response)


def commandFURL():
    check = checkAll(sender, text, 2, [2], 1)
    if check:
        search = findAccountURL(check)
        if search:
            response = f'Имя профиля: {search["personaname"]}\n' \
                       f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                       f'Steam64: {search["steamid"]}\n' \
                       f'URL: {search["profileurl"]}'
            vk.sendMessage(sender, messages['find']['success'] + response)



def commandProfile():
    if checkAll(sender, text, 1, None, None):
        steam32 = checkUserlist(sender)
        if steam32:
            search = findAccountID(steam32)
            response = messages['find']['success'] + f'Имя профиля: {search["personaname"]}\n' \
                       f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                       f'Steam64: {search["steamid"]}\n' \
                       f'URL: {search["profileurl"]}'
        else:
            response = messages['check_errors']['not_link']
        vk.sendMessage(sender, response)


def commandCheckQuest(sender, text):
    check = checkAll(sender, text, 2, [1], 1)
    if check:
        # check - id
        q = getQuests()
        aid = checkUserlist(sender)
        if aid:
            for checkquest in q:
                if checkquest['id'] == int(check):
                    qid = checkquest['id']
                    if sender in checkquest['users_complete']:
                        vk.sendMessage(sender, messages['quests']['already_complete'])
                        return
                    _type = [checkquest['type'], checkquest['type_more']]
                    reward = checkquest['reward']
                    # vk.sendMessage(sender, messages['matches']['wait'])
                    complete = True
                    if _type[0] == 1: # победы
                        matches = getHistory(aid, matches_requested=_type[1], json=True)
                        for match in matches:
                            if not match[0]:
                                complete = False

                        if complete:
                            completeQuest(sender, qid - 1)
                            users = getUsers()
                            for user in users:
                                if user['vk'] == sender:
                                    user['balance'] += reward
                                    break
                            vk.sendMessage(sender, messages['quests']['complete'])
                        else:
                            vk.sendMessage(sender, messages['quests']['not_complete'])
                    elif _type[0] == 2: # победа на герое
                        pass
                    elif _type[0] == 3: # несколько побед на герое подряд
                        pass
        else:
            vk.sendMessage(sender, messages['check_errors']['not_link'])
    else:
        vk.sendMessage(sender, messages['check_errors']['error_args'])


def commandQuest(sender, text, showcomplete=False):
    if checkAll(sender, text, 1, None, None):
        if showcomplete:
            users = getUsers()
            find = False
            for user in users:
                if user['vk'] == sender:
                    find = True
                    break
            if find:
                response = messages['quests']['list_complete'] + Quests(sender, showcomplete=True)
            else:
                response = messages['check_errors']['not_link']
        else:
            response = messages['quests']['list_not_complete'] + Quests(sender)
    else:
        check = checkAll(sender, text, 2, [1], 1)
        if check:
            response = Quests(sender, check)
            if not response:
                response = messages['quests']['not_found']
    vk.sendMessage(sender, response)

def commandLastHeroMatches():
    # не привязанный акк
    check = checkAll(sender, text, 4, [1, 2, 1], 1)
    if check:
        if 1 <= int(text[3]) <= 10:
            hero_id = getHeroes(hero_name=text[2].title())
            if hero_id:
                response = getHistory(int(check), hero_id, int(text[3]))
                if response:
                    response = messages['matches']['last'] + response
                else:
                    response = messages['matches']['error']
            else:
                response = messages['matches']['error_hero']
        else:
            response = messages['matches']['match_count']
    else:
        check = checkAll(sender, text, 3, [2, 1], 1)
        if check:
            player = checkUserlist(sender)
            if player:
                if 1 <= int(text[2]) <= 10:
                    hero_id = getHeroes(hero_name=text[1].title())
                    if hero_id:
                        response = getHistory(player, hero_id, int(text[2]))
                        if response:
                            response = messages['matches']['last'] + response
                        else:
                            response = messages['matches']['error']
                    else:
                        response = messages['matches']['error_hero']
                else:
                    response = messages['matches']['match_count']
            else:
                response = messages['check_errors']['not_link']
        else:
            response = messages['check_errors']['error_args']
    vk.sendMessage(sender, response)


def commandLastMatches():
    check = checkAll(sender, text, 2, [1], 1)
    if check:
        check = checkUserlist(sender)
        if check:
            if 1 <= int(text[1]) <= 10:
                vk.sendMessage(sender, messages['matches']['wait'])
                response = getHistory(account_id=check, matches_requested=int(text[1]))
                if response:
                    response = messages['matches']['last'] + response
                else:
                    response = messages['matches']['error']
            else:
                response = messages['matches']['match_count']
        else:
            response = messages['check_errors']['not_link']
    else:
        check = checkAll(sender, text, 3, [1, 1], 1)
        if check:
            if 1 <= int(text[2]) <= 10:
                steam32 = int(text[1])
                vk.sendMessage(sender, messages['matches']['wait'])
                response = getHistory(account_id=steam32, matches_requested=int(text[2]))
                if response:
                    response = messages['matches']['last'] + response
                else:
                    response = messages['matches']['error']
            else:
                response = messages['matches']['match_count']
        else:
            response = messages['check_errors']['error_args']
    vk.sendMessage(sender, response)


# API.APIHelp()
connectUsers()
connectHeroes()
connectQuests()
try:
    while True:
        msg = getMessage()
        if msg:
            print('📎 log: ' + str(msg))
            sender, text = msg
            if text[0] == '/add':
                commandAdd()
            elif text[0] == '/delete' or text[0] == '/del':
                commandDel()
            elif text[0] == '/findid' or text[0] == '/fid':
                commandFID()
            elif text[0] == '/findurl' or text[0] == '/furl':
                commandFURL()
            elif text[0] == '/profile':
                commandProfile()
            elif text[0] == '/help':
                response = messages['help']['help_text']
                for command in messages['help']['commands_description']:
                    for cmd in command:
                        response += f'{cmd}: {command[cmd]}\n'
                vk.sendMessage(sender, response)
            elif text[0] == '/lastmatches' or text[0] == '/lm':
                commandLastMatches()
            elif text[0] == '/lastmatcheshero' or text[0] == '/lmh':
                commandLastHeroMatches()
            elif text[0] == '/match' or text[0] == '/m':
                check = checkAll(sender, text, 2, 1, 1)
                if check:
                    vk.sendMessage(sender, messages['matches']['wait'])
                    response = getMatchInfo(text[1])
                    response = messages['matches']['current'] + response
                    vk.sendMessage(sender, response)
            elif text[0] == '/quest' or text[0] == '/q':
                commandQuest(sender, text)
            elif text[0] == '/questcheck' or text[0] == '/qch':
                commandCheckQuest(sender, text)
            elif text[0] == '/questcomplete' or text[0] == '/qc':
                commandQuest(sender, text, showcomplete=True)
            elif text[0] == '/balance':
                users = getUsers()
                find = False
                for user in users:
                    if user['vk'] == sender:
                        find = True
                        vk.sendMessage(sender, f'Ваш баланс: {user["balance"]}')
                if not find:
                    vk.sendMessage(sender, messages['check_errors']['not_link'])
            else:
                vk.sendMessage(sender, messages['check_errors']['command_notfound'])
except Exception as ex:
    print('[!]'+str(ex))
    vk.sendMessage(sender, messages['check_errors']['fatal_error'])
except KeyboardInterrupt:
    print('Завершение...')
finally:
    disconnectUsers()
    disconnectQuests()

# 4 - rank all pick
# 2 - cap mode
# 3 - random draft
# 22 - all pick
# 23 - turbo
