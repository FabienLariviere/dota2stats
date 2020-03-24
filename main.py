from commands import *

conf = connectConfig()
messages = conf['messages']
token = conf['keys']['vk_token']
group_id = conf['keys']['vk_group']

vk = API.VK(token, group_id)

try:
    connectUsers()
    print('Пользователи загружены '+str(len(getUsers())))
    connectHeroes()
    print('Герои загружены')
    while True:
        event = vk.getUpdate()
        if event['updates']:
            msg = vk.decodeUpdate(event)
            if msg and msg[1][0] == '/':
                sender, text = msg
                text = text.split(' ')
                print(sender, text)
                if text[0] == '/add':
                    if checkLenght(text, 2):
                        if checkSymbols(text[1], 1):
                            check = checkUserlist(sender)
                            if not check:
                                steam32 = findAccountID(text[1])
                                if steam32:
                                    addUser(sender, int(text[1]))
                                    vk.sendMessage(sender, messages['add']['success'])
                                else:
                                    vk.sendMessage(sender, messages['add']['not_found'])
                            else:
                                vk.sendMessage(sender, messages['add']['error'])
                        else:
                            vk.sendMessage(sender, messages['check_errors']['need_numbers'])
                    else:
                        vk.sendMessage(sender, messages['check_errors']['error_args'])
                elif text[0] == '/del' or text[0] == '/delete':
                    check = checkUserlist(sender)
                    if check:
                        delUser(sender)
                        vk.sendMessage(sender, messages['delete']['success'])
                    else:
                        vk.sendMessage(sender, messages['delete']['error'])
                elif text[0] == '/findid' or text[0] == '/fid':
                    if checkLenght(text, 2):
                        if checkSymbols(text[1], 1):
                            search = findAccountID(text[1])
                            if search:
                                response = f'Имя профиля: {search["personaname"]}\n' \
                                           f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                                           f'Steam64: {search["steamid"]}\n' \
                                           f'URL: {search["profileurl"]}'
                                vk.sendMessage(sender, messages['find']['success']+response)
                            else:
                                vk.sendMessage(sender, messages['find']['error32'])
                        else:
                            vk.sendMessage(sender, messages['check_errors']['need_numbers'])
                    else:
                        vk.sendMessage(sender, messages['check_errors']['error_args'])
                elif text[0] == '/findurl' or text[0] == '/furl':
                    if checkLenght(text, 2):
                        search = findAccountURL(text[1])
                        if search:
                            response = f'Имя профиля: {search["personaname"]}\n' \
                                       f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                                       f'Steam64: {search["steamid"]}\n' \
                                       f'URL: {search["profileurl"]}'
                            vk.sendMessage(sender, messages['find']['success']+response)
                        else:
                            vk.sendMessage(sender, messages['find']['errorurl'])
                    else:
                        vk.sendMessage(sender, messages['check_errors']['error_args'])
                elif text[0] == '/profile':
                    steam32 = ''
                    find = False
                    for user in getUsers():
                        if user['vk'] == sender:
                            steam32 = user['steam32']
                            find = True
                    if find:
                        search = findAccountID(steam32)
                        response = f'Имя профиля: {search["personaname"]}\n' \
                                   f'Steam32: {str(int(search["steamid"]) - 76561197960265728)}\n' \
                                   f'Steam64: {search["steamid"]}\n' \
                                   f'URL: {search["profileurl"]}'
                        vk.sendMessage(sender, messages['find']['success']+response)
                    else:
                        vk.sendMessage(sender, messages['check_errors']['not_link'])
                elif text[0] == '/help':
                    response = messages['help']['help_text']
                    for command in messages['help']['commands_description']:
                        for cmd in command:
                            response += (f'{cmd}: {command[cmd]}\n')
                    vk.sendMessage(sender, response)
                elif text[0] == '/lastmatches' or text[0] == '/lm':
                    if checkLenght(text, 2):
                        if checkSymbols(text[1], 1):
                            if 1 <= int(text[1]) <= 10:
                                steam32 = ''
                                find = False
                                for user in getUsers():
                                    if user['vk'] == sender:
                                        steam32 = user['steam32']
                                        find = True
                                if find:
                                    response = getHistory(account_id=steam32, matches_requested=int(text[1]))
                                    response = messages['matches']['last'] + response
                                    vk.sendMessage(sender, response)
                                else:
                                    vk.sendMessage(sender, messages['check_errors']['not_link'])
                            else:
                                vk.sendMessage(sender, 'Вам доступно количество матчей 1-10')
                        else:
                            vk.sendMessage(sender, messages['check_errors']['need_numbers'])
                    # elif checkLenght(text, 3):
                    #
                    else:
                        vk.sendMessage(sender, messages['check_errors']['error_args'])
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
