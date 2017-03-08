import requests

def getOverwatch(username, region = 'us', which = 'qp'):
    if region == '':
        reigon = 'us'
    url = 'https://owapi.net/api/v3/u/' + username + '/stats?platform=xbx'
    data = requests.get(url, headers={'user-agent': 'kohaibot/1.3.0'}).json()
    win_rate = data[region]['stats'][which]['overall_stats']['win_rate']
    rank = data[region]['stats'][which]['overall_stats']['comprank']
    avatar = data[region]['stats'][which]['overall_stats']['avatar']
    wins = data[region]['stats'][which]['overall_stats']['wins']
    losses = data[region]['stats'][which]['overall_stats']['losses']
    return avatar, rank, win_rate, wins, losses
