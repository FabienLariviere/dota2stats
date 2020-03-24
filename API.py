import requests

key = '1C44A09A58FF482AF0582D9A85D4ABE9'


def APIHelp():
    d = requests.get('http://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v1/', params={
        'key': key
    }).json()
    for t in d['apilist']['interfaces']:
        print('' + t['name'])
        for m in t['methods']:
            print('\t' + m['name'])
            for p in m['parameters']:
                print('\t\t' + p['name'])


def sysAddHeroes():
    return requests.get('https://api.opendota.com/api/heroes').json()


class VK:
    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id

    def sendMessage(self, user, message):
        response = requests.get('https://api.vk.com/method/messages.send', params={
            'access_token': self.token,
            'peer_id': user,
            'random_id': 0,
            'message': message,
            'group_id': self.group_id,
            'v': '5.103'
        }).json()

    def getUpdate(self):
        data = requests.get('https://api.vk.com/method/messages.getLongPollServer', params={
            'access_token': self.token,
            'group_id': self.group_id,
            'v': '5.103'}).json()['response']

        update = requests.get('https://' + data['server'], params={
            'act': 'a_check',
            'wait': '25',
            'mode': '3',
            'key': data['key'],
            'ts': data['ts'],
            'version': '3'}).json()
        # print(data)
        # print(update)
        return update

    def decodeUpdate(self, update):
        for element in update['updates']:
            code = element[0]
            if code == 4:
                get_flags = element[2]
                flags = []
                sender = element[3]
                timestamp = element[4]
                text = element[5]
                for number in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 65536, 131072, 262144]:
                    if get_flags & number:
                        flags.append(number)
                        decode_msg = (code, flags, sender, timestamp, text)
                        if decode_msg[0] == 4 and 2 not in decode_msg[1]:
                            return [decode_msg[2], decode_msg[4]]
                        else:
                            return False


class Steam:
    def findAccountID(self, steamid):
        response = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/', params={
            'steamids': steamid,
            'key': key
        }).json()['response']
        return response

    def findAccountURL(self, steamname):
        response = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/', params={
            'vanityurl': steamname,
            'key': key
        }).json()['response']
        return response


class Dota:
    def getServerStreamID(self, steamid):
        response = requests.get('http://api.steampowered.com/IDOTA2StreamSystem_570/GetBroadcasterInfo/v1/', params={
            'broadcaster_steam_id': steamid,
            'key': key
        }).json()
        return response

    def getLiveMatchInfo(self, streamid):
        response = requests.get('http://api.steampowered.com/IDOTA2MatchStats_570/GetRealtimeStats/v1/', params={
            'server_steam_id': streamid,
            'key': key
        }).json()
        return response

    def getMatchInfo(self, match_id):
        response = requests.get('http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/', params={
            'match_id': match_id,
            'include_persona_names': 1,
            'key': key
        }).json()['result']
        return response

    def getHistory(self, account_id=None, hero_id=None, matches_requested=25):
        response = requests.get('http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/', params={
            'hero_id': hero_id,
            'account_id': account_id,
            'matches_requested': matches_requested,
            'key': key
        }).json()['result']
        return response
