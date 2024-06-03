from ssl import SSLError

import threading
import time
import requests

from .models import Game, GameList, db 
from . import scheduler




def get_games_steamweb():
    with scheduler.app.app_context():
        # WEBAPIKEY = 'ECF5EA6F18F37B8600102FE342FA06AD'
        url='https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        threading.Thread(target=insert_gameId_data,args=(url,)).start()
        threading.Thread(target=update_game_details,args=()).start()

def insert_gameId_data(url):

    with scheduler.app.app_context():
        #drop every row in table
        db.session.query(GameList).delete()
        db.session.commit()
        
        data = get_request(url)
        apps = data['applist']['apps']
        
        for appSteam in apps:
            if appSteam['name'] == '': continue
            game = GameList(
                game_id = appSteam['appid'],
                game_name = appSteam['name']
            )
            db.session.add(game)
        db.session.commit()
        

def get_request(url, parameters=None):
    """Return json-formatted response of a get request using optional parameters.
    
    Parameters
    ----------
    url : string
    parameters : {'parameter': 'value'}
        parameters to pass as part of get request
    
    Returns
    -------
    json_data
        json-formatted response (dict-like)
    """
    try:
        response = requests.get(url=url, params=parameters)
    except SSLError as s:
        print('SSL Error:', s)
        
        for i in range(5, 0, -1):
            print('\rWaiting... ({})'.format(i), end='')
            time.sleep(1)
        print('\rRetrying.' + ' '*10)
        
        # recusively try again
        return get_request(url, parameters)
    
    if response:
        return response.json()
    else:
        # response is none usually means too many requests. Wait and try again 
        print('No response, waiting 10 seconds...')
        time.sleep(10)
        print('Retrying.')
        return get_request(url, parameters)
def parse_steam_request(appid):
    """Unique parser to handle data from Steam Store API.
    
    Returns : json formatted data (dict-like)
    """
    url = "http://store.steampowered.com/api/appdetails/"
    parameters = {"appids": appid, "cc": "th", "l": "thai"}
    json_data = get_request(url, parameters=parameters)
    json_app_data = json_data[str(appid)]
    
    if json_app_data['success']:
        data = json_app_data['data']
    else:
        data = {'steam_appid': appid}
        
    return data
def update_game_details():
    with scheduler.app.app_context():

        db.session.query(Game).delete()
        db.session.commit()
        for i in range(7):
            steamSpyDataAll = get_request('https://steamspy.com/api.php?request=all&page='+str(i))


            for appid , game_info in steamSpyDataAll.items():
            
                game_genre = ''
                data = parse_steam_request(appid)
                
                genres_data = data.get('genres', [])
                for genre in genres_data:
                    game_genre += genre['description']+','
                # print(game_genre)
                game = Game(
                    game_id = appid,
                    game_name = data.get('name', 'N/A'),
                    is_free = data.get('is_free', 0),
                    image = data.get('header_image', 'N/A'),
                    short_description = data.get('short_description', 'N/A'),
                    price = data.get('price_overview', {}).get('final_formatted', 'N/A'),
                    discount_percent = data.get('price_overview', {}).get('discount_percent', 'N/A'),
                    genres = game_genre,
                    
                    developer = game_info.get('developer', 'N/A'),
                    review_positive = game_info.get('positive', -1),
                    review_negative = game_info.get('negative', -1),
                )
                db.session.add(game)
                db.session.commit()
                
