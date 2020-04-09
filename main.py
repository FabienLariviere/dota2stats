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
    check = checkAll(sender, text, search=True)
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
def commandFID():
    check = checkAll(sender, text, symbol=1, search=True)
    if check:
        search = findAccountID(check)
        if search:
            response = f'Имя профиля: {search["personaname"]}\n' \
                       f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                       f'Steam64: {search["steamid"]}\n' \
                       f'URL: {search["profileurl"]}'
            vk.sendMessage(sender, messages['find']['success'] + response)
def commandFURL():
    check = checkAll(sender, text, symbol=2, search=True)
    if check:
        search = findAccountURL(check)
        if search:
            response = f'Имя профиля: {search["personaname"]}\n' \
                       f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                       f'Steam64: {search["steamid"]}\n' \
                       f'URL: {search["profileurl"]}'
            vk.sendMessage(sender, messages['find']['success'] + response)
def commandProfile():
    check = checkAll(sender, text, 1, search=True)
    if check:
        search = findAccountID(check)
        response = f'Имя профиля: {search["personaname"]}\n' \
                   f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                   f'Steam64: {search["steamid"]}\n' \
                   f'URL: {search["profileurl"]}'
        vk.sendMessage(sender, messages['find']['success'] + response)
def commandLastMatches():
    check = checkAll(sender, text)
    if check:
        if 1 <= int(text[1]) <= 10:
            vk.sendMessage(sender, messages['matches']['wait'])
            response = getHistory(account_id=check, matches_requested=int(text[1]))
            if response:
                response = messages['matches']['last'] + response
            else:
                response = messages['matches']['error']
            vk.sendMessage(sender, response)
        else:
            vk.sendMessage(sender, 'Вам доступно количество матчей 1-10')
    else:
        check = checkAll(sender, text, 3)
        if check:
            if checkSymbols(text[1], 1):
                check = findAccountID(text[1])
                if 1 <= int(text[2]) <= 10:
                    steam32 = int(text[1])
                    vk.sendMessage(sender, messages['matches']['wait'])
                    response = getHistory(account_id=steam32, matches_requested=int(text[2]))
                    if response:
                        response = messages['matches']['last'] + response
                    else:
                        response = messages['matches']['error']
                    vk.sendMessage(sender, response)
                else:
                    vk.sendMessage(sender, 'Вам доступно количество матчей 1-10')
# API.APIHelp()
try:
    connectUsers()
    print('Пользователи загружены '+str(len(getUsers())))
    connectHeroes()
    print('Герои загружены')
    while True:
        msg = getMessage()
        if msg:
            print('📎 log: '+str(msg))
            sender, text = msg
            if text[0] == '/add':
                commandAdd()
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
            elif text[0] == '/match' or text[0] == '/m':
                check = checkAll(sender, text)
                if check:
                    vk.sendMessage(sender, messages['matches']['wait'])
                    response = getMatchInfo(text[1])
                    response = messages['matches']['current'] + response
                    vk.sendMessage(sender, response)
            else:
                vk.sendMessage(sender, messages['check_errors']['command_notfound'])
except KeyboardInterrupt:
    disconnectUsers()
    print('Пользователи сохранены')

# 4 - rank all pick
# 2 - cap mode
# 3 - random draft
# 22 - all pick
# 23 - turbo
