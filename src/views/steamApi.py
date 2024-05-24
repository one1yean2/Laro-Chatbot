# from concurrent.futures import ThreadPoolExecutor
# from flask import Blueprint , current_app ,request
# from sqlalchemy import update
# from ..models import Game, db
# import requests
# import threading
# import time

# bp = Blueprint("steamApi", __name__, url_prefix="/steamApi")
# # TODO: USING KAFKA TO SEND EVENT 
# @bp.route("/", methods=["POST"])
# def get_games():
#     page = request.args.get("page", 0, type=int)
#     # Create and start a new thread for inserting game data
#     app = current_app._get_current_object()
#     get_game_data_from_steamspy_thread = threading.Thread(target=get_game_data_from_steamspy,args=(app,page))
#     get_game_data_from_steamspy_thread.start()

#     return {"message": "Data insertion is complete"}, 200


# def get_game_data_from_steamspy(app,page):
#     with app.app_context():
#         url = "https://steamspy.com/api.php?request=all&page="+str(page)
#         response = requests.get(url)
#         data = response.json()
        
#         # Get existing game IDs from the database
#         existing_game_ids = {game.appid for game in Game.query.all()}
        
#         # Insert data into the database for new games
#         with ThreadPoolExecutor (max_workers=10) as executor:
#             for appid, game_data in data.items():
#                 # Check if the game is not already in the database
#                 if int(appid) not in existing_game_ids:
#                     # executor.submit(test,app,game_data,appid)
#                 # threading.Thread(target=test,args=(app,game_data,appid)).start()

#                     game = Game(
#                         appid=int(appid),
#                         name=game_data.get('name'),
#                         developer=game_data.get('developer'),
#                         publisher=game_data.get('publisher'),
#                         score_rank=game_data.get('score_rank'),
#                         positive=game_data.get('positive'),
#                         negative=game_data.get('negative'),
#                         price=game_data.get('price'),
#                         initialprice=game_data.get('initialprice'),
#                         discount=game_data.get('discount'),
#                     )
#                     db.session.add(game)
#                     db.session.commit()
            
            
                    
#                     url = f"https://store.steampowered.com/api/appdetails/?appids={appid}"
#                     response = requests.get(url)
#                     data = response.json()

                    
#                     if not data[str(appid)]['success']:
#                         print(f"Failed to fetch data for appid {appid}")
#                         continue
#                         # return

#                     app_data = data[str(appid)]['data']

#                     if app_data['type'] == 'game':
#                         print(app_data['type'])
#                         values = {}
#                         prices = app_data.get('price_overview', {})
#                         values.update(
#                             {
#                                 'is_free' : app_data.get('is_free', 0),
#                                 'detailed_description' : app_data.get('detailed_description', ''),
#                                 'about_the_game':app_data.get('about_the_game', ''),
#                                 'short_description':app_data.get('short_description', ''),
#                                 'header_image':app_data.get('header_image', ''),
#                                 'website':app_data.get('website', ''),
#                                 'discount_percent' : prices.get('discount_percent', 0),
#                                 'final_formatted' : prices.get('final_formatted', ''),
#                             }
#                         )
#                         db.session.execute(
#                             update(Game).where(
#                                 Game.appid == appid,
#                             ).values(values)
#                         )

#                         db.session.commit()
#                         print(f"Data for appid {appid} stored successfully")
                
#                 # url = f"https://store.steampowered.com/api/appdetails/?appids={appid}"
#                 # response = requests.get(url)
#                 # data = response.json()
#                 # print(data)
#                 # fetch_and_store_data(app,appid)
#                 # fetch_from_steam_thread = threading.Thread(target=fetch_and_store_data,args=(app,appid))
#                 # fetch_from_steam_thread.start()
#                 # get_game_data_from_steam(app,appid)
# # def get_game_data_from_steam(app,appid):

# def test(app,game_data,appid):
#     with app.app_context():
#         game = Game(
#                     appid=int(appid),
#                     name=game_data.get('name'),
#                     developer=game_data.get('developer'),
#                     publisher=game_data.get('publisher'),
#                     score_rank=game_data.get('score_rank'),
#                     positive=game_data.get('positive'),
#                     negative=game_data.get('negative'),
#                     price=game_data.get('price'),
#                     initialprice=game_data.get('initialprice'),
#                     discount=game_data.get('discount'),
#                 )
#         db.session.add(game)
#         db.session.commit()
#         urlFromSteam = f"https://store.steampowered.com/api/appdetails/?appids={appid}"
#         responseFromSteam = requests.get(urlFromSteam)
#         dataFromSteam = responseFromSteam.json()
#         # print(data)
#         if not dataFromSteam[str(appid)]['success']:
#             print(f"Failed to fetch data for appid {appid}")
#             # continue
#             return

#         app_data = dataFromSteam[str(appid)]['data']
        
#         if app_data['type'] == 'game':
#             print(app_data['type'])
#             values = {}
#             prices = app_data.get('price_overview', {})
#             values.update(
#                 {
#                     'is_free' : app_data.get('is_free', 0),
#                     'detailed_description' : app_data.get('detailed_description', ''),
#                     'about_the_game':app_data.get('about_the_game', ''),
#                     'short_description':app_data.get('short_description', ''),
#                     'header_image':app_data.get('header_image', ''),
#                     'website':app_data.get('website', ''),
#                     'discount_percent' : prices.get('discount_percent', 0),
#                     'final_formatted' : prices.get('final_formatted', ''),
#                 }
#             )
#             db.session.execute(
#                 update(Game).where(
#                     Game.appid == appid,
#                 ).values(values)
#             )

#             db.session.commit()
#             return f"Data for appid {appid} stored successfully"
# def fetch_and_store_data(app,app_id):
#     with app.app_context():
    
#         url = f"https://store.steampowered.com/api/appdetails/?appids={app_id}"
#         response = requests.get(url)
#         data = response.json()
#         print(data)
#         if not data[str(app_id)]['success']:
#             print(f"Failed to fetch data for appid {app_id}")
#             return

#         app_data = data[str(app_id)]['data']
#         prices_data = app_data['price_overview'],
#         values = {}
        
#         values.update(
#             {
#                 # 'is_free' : app_data.get('is_free', 0),
#                 # 'detailed_description' : app_data.get('detailed_description', ''),
#                 # 'about_the_game':app_data.get('about_the_game', ''),
#                 # 'short_description':app_data.get('short_description', ''),
#                 # 'header_image':app_data.get('header_image', ''),
#                 # 'website':app_data.get('website', ''),
#                 'discount_percent' : prices_data['discount_percent'],
#                 'final_formatted' : prices_data['final_formatted'],
#             }
#         )
#         db.session.execute(
#             update(Game).where(
#                 Game.appid == app_id,
#             ).values(values)
#         )

#         db.session.commit()
#         print(f"Data for appid {app_id} stored successfully")
# def get_game_data_from_steam(app,appid):
#     with app.app_context():
#         url = "https://store.steampowered.com/api/appdetails/?appids="+str(appid)
#         response = requests.get(url)
#         data = response.json()
#         print(data)
#         # Get existing game IDs from the database
#         # existing_game_ids = {game.appid for game in Game.query.all()}
        
#         # # Insert data into the database for new games
#         # for appid, game_data in data.items():
#         #     # Check if the game is not already in the database
#         #     if int(appid) not in existing_game_ids:
#         #         game = Game(
#         #             appid=int(appid),
#         #             name=game_data.get('name'),
#         #             developer=game_data.get('developer'),
#         #             publisher=game_data.get('publisher'),
#         #             score_rank=game_data.get('score_rank'),
#         #             positive=game_data.get('positive'),
#         #             negative=game_data.get('negative'),
#         #             userscore=game_data.get('userscore'),
#         #             owners=game_data.get('owners'),
#         #             average_forever=game_data.get('average_forever'),
#         #             average_2weeks=game_data.get('average_2weeks'),
#         #             median_forever=game_data.get('median_forever'),
#         #             median_2weeks=game_data.get('median_2weeks'),
#         #             price=game_data.get('price'),
#         #             initialprice=game_data.get('initialprice'),
#         #             discount=game_data.get('discount'),
#         #         )
#         #         db.session.add(game)
#         #         db.session.commit()
        
# # @bp.route("/<sid>", methods=["POST"])
# # def update_subject(sid: int):
# #     print(sid)
# #     subject = db.session.get(Subject, sid)
# #     if subject is None:
# #         raise InvalidSubjectID()

# #     name = request.form.get("name", "")
# #     professor = request.form.get("professor", "")
# #     print(name)
# #     print(professor)

# #     values = {}
# #     if not name.isspace():
# #         values.update(
# #             {
# #                 "name": name
# #             }
# #         )

# #     if not professor.isspace():
# #         values.update(
# #             {
# #                 "professor": professor,
# #             }
# #         )

# #     print(values)
# #     db.session.execute(
# #         update(Subject).where(
# #             Subject.id == sid
# #         ).values(values)
# #     )
# #     db.session.commit()

# #     return redirect(url_for("subject.subject"))



import threading
import time
from flask import Blueprint,current_app
import requests
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import update
from ..models import db, Game  # Adjust the import based on your app structure


bp = Blueprint("steamApi", __name__, url_prefix="/steamApi")



def fetch_steamspy_data(page):
    url = f"https://steamspy.com/api.php?request=all&page={page}"
    response = requests.get(url)
    return response.json()
def fetch_steamspy_data_detail(appid):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    response = requests.get(url)
    return response.json()

def fetch_steamstore_data(appid):
    url = f"https://store.steampowered.com/api/appdetails/?appids={appid}"
    response = requests.get(url)

    return response.json()

def insert_game_data(app, game_data, appid):
    with app.app_context():
        detail = fetch_steamspy_data_detail(appid)
        
        game = Game(
            appid=int(appid),
            name=game_data.get('name'),
            developer=game_data.get('developer'),
            publisher=game_data.get('publisher'),
            positive=game_data.get('positive'),
            negative=game_data.get('negative'),
            price=game_data.get('price'),
            initialprice=game_data.get('initialprice'),
            discount=game_data.get('discount'),
            languages = detail.get('languages'),
            genre = detail.get('genre'),
        )
        db.session.add(game)
        db.session.commit()
        

def update_game_details(app, appid, app_data):
    with app.app_context():
        if app_data['type'] == 'game':
            prices = app_data.get('price_overview', {})
            values = {
                'is_free': app_data.get('is_free', 0),
                'detailed_description': app_data.get('detailed_description', ''),
                'about_the_game': app_data.get('about_the_game', ''),
                'short_description': app_data.get('short_description', ''),
                'header_image': app_data.get('header_image', ''),
                'website': app_data.get('website', ''),
                'discount_percent': prices.get('discount_percent', 0),
                'final_formatted': prices.get('final_formatted', ''),
            }
            db.session.execute(
                update(Game).where(Game.appid == appid).values(values)
            )
            db.session.commit()
            print(f"Data for appid {appid} stored successfully")
            

def get_game_detail_from_steamstore(app):
    with app.app_context():
        
        existing_game_ids = {game.appid for game in Game.query.all()}
        
        for appid in existing_game_ids:
            store_data = fetch_steamstore_data(appid)
            if not store_data[str(appid)]['success']:
                print(f"Failed to fetch data for appid {appid}")
                
            else:
                app_data = store_data[str(appid)]['data']
                update_game_details(app, appid, app_data)
                time.sleep(1)

def get_game_data_from_steamspy(app, page):
    with app.app_context():
        data = fetch_steamspy_data(page)
        
        existing_game_ids = {game.appid for game in Game.query.all()}
        
        # with ThreadPoolExecutor(max_workers=10) as executor:
        for appid, game_data in data.items():
            if int(appid) not in existing_game_ids:
                # detail = fetch_steamspy_data_detail(appid)
                threading.Thread(target=insert_game_data,args=(app, game_data, int(appid))).start()
                # executor.submit(insert_game_data, app, game_data,detail, int(appid))

@bp.route("/", methods=["GET"])
def get_games():
    
    app = current_app._get_current_object()
    get_game_data_from_steamspy_thread = threading.Thread(target=get_game_data_from_steamspy,args=(app,0))
    get_game_data_from_steamspy_thread.start()
    return {"message": "Data insertion is complete"}, 200
@bp.route("/steam",methods=["GET"])
def get_games_steam():
    app = current_app._get_current_object()
    get_game_data_from_steamstore_thread = threading.Thread(target=get_game_detail_from_steamstore,args=(app,))
    get_game_data_from_steamstore_thread.start()
    return {"message": "Data insertion is complete"}, 200