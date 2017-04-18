import requests
from config import osuKey

def getOsu(username, mode = 0):
    url = 'https://osu.ppy.sh/api/get_user?k=' + osuKey() + '&m=' + str(mode) + '&u=' + username
    response = requests.get(url, verify=True)
    data = response.json()
    username = data[0]['username']
    user_id = data[0]['user_id']
    pp_raw = data[0]['pp_raw']
    accuracy = data[0]['accuracy']
    pp_rank = data[0]['pp_rank']
    country_rank = data[0]['pp_country_rank']
    country = data[0]['country']
    avatar = 'http://s.ppy.sh/a/' + str(user_id)
    return username, user_id, pp_raw, pp_rank, accuracy, country_rank, country
