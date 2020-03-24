from commands import *

token = 'a411be2417bcdc9f4abbfa7c733273c0035492052ee699e0252f2cbad4cafa969ea8d4ea606fa01c3bd52'
group_id = 188677997

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
                if text[0] == '/add' and len(text) == 2:
                    check = checkUserlist(sender)
                    if not check:
                        steam32 = getAccount(text[1])
                        if steam32:
                            addUser(sender, int(text[1]))
                            vk.sendMessage(sender, f'📥 SteamID {text[1]} успешно привязан к вашему аккаунту')
                        else:
                            vk.sendMessage(sender, '🔎 Пользователь не найден')
                    else:
                        vk.sendMessage(sender, f'📦 К Вашему аккаунту уже привязан SteamID {check}')
                elif text[0] == '/del' or 'delete':
                    check = checkUserlist(sender)
                    if check:
                        delUser(sender)
                        vk.sendMessage(sender, '📤 SteamID отвязан от Вашего аккаунта')


except KeyboardInterrupt:
    disconnectUsers()
    print('Пользователи сохранены')
# getAccount(174599477)
# findAccount('fabien_lariviere')
# API.APIHelp()
# print(API.test())

# getHistory()
# getHistory(matches_requested=25)
# getMatchInfo(5311196191)
# dota = API.Dota()

# vk.sendMessage(428435813, '123')
# 4 - rank all pick
# 2 - cap mode
# 3 - random draft
# 22 - all pick
# 23 - turbo
