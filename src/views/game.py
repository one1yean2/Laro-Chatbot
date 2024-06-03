from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, jsonify , request
from random import shuffle

from src.producer import noti_produce
from src.steamdata import get_request, parse_steam_request
from ..models import Game, db
import pandas as pd
from .custom_payload_format.format import custompayload, error_payload_format, format_game_detail_flex, format_game_flex

bp = Blueprint("game", __name__, url_prefix="/game")

@bp.route("/genre", methods=["GET"])
def get_game_genre():
    customer_id = request.args.get("customer_id")
    noti_produce(customer_id)
    df = pd.read_sql_query('SELECT DISTINCT genres FROM game',db.engine)
    df['genre_split'] = df['genres'].str.split(',')
    df_exploded = df.explode('genre_split')
    df_exploded = df_exploded[df_exploded['genre_split'] != '']
    
    genre = df_exploded['genre_split'].unique()
    genre_list = genre.tolist()
    shuffle(genre_list)
    game_carousel = format_game_flex(genre_list)
    
    out = custompayload(game_carousel)

    
    return jsonify(out) , 200


    
@bp.route("/", methods=["GET"])
def get_games_from_genre():
    customer_id = request.args.get("customer_id")
    noti_produce(customer_id)
    genre_data = request.args.get("genre")
    genre = genre_data.split(" ")[1]
    with ThreadPoolExecutor() as executor:
        query = f'SELECT game_id ,price ,developer ,discount_percent ,image , genres ,game_name ,review_negative ,short_description,review_positive FROM game WHERE genres LIKE "%{genre}%"'
   
        future = executor.submit(fetch_games,query, db.engine)
        df = future.result()
      
    if df == "Game not found":
      err = format_game_flex("error")
      out = custompayload(err)
      return jsonify(out) , 200
  
    games = format_game_detail_flex(df)
    out = custompayload(games)

    return jsonify(out) , 200





@bp.route("/search", methods=["GET"])
def search_game():
    game_name = request.args.get("game_name")
    customer_id = request.args.get("customer_id")
    noti_produce(customer_id)
    if len(game_name) <= 3:
        return error_payload_format("กรุณากรอกข้อมูลอย่างน้อย 4 ตัวอักษร"), 200
    
    query = f'SELECT game_id ,game_name FROM gamelist WHERE game_name LIKE "%{game_name}%"'

    games = fetch_games(query, db.engine)
    for game in games[:10]:
        # print(game.get("game_id"))
        g = Game.query.filter_by(game_id=game.get('game_id')).first()
        game_genre = ''
        steamSpyData = get_request('https://steamspy.com/api.php?request=appdetails&appid='+str(game['game_id']))
        if g is None:
            data = parse_steam_request(game.get('game_id'))
            genres_data = data.get('genres', [])
            for genre in genres_data:
                game_genre += genre['description']+','
            mygame = Game(
                game_id = game.get('game_id'),
                game_name = data.get('name', 'N/A'),
                is_free = data.get('is_free', 0),
                image = data.get('header_image', 'N/A'),
                short_description = data.get('short_description', 'N/A'),
                price = data.get('price_overview', {}).get('final_formatted', 'N/A'),
                discount_percent = data.get('price_overview', {}).get('discount_percent', 'N/A'),
                genres = game_genre,
                
                developer = steamSpyData.get('developer', 'N/A'),
                review_positive = steamSpyData.get('positive', -1),
                review_negative = steamSpyData.get('negative', -1),
            )
            db.session.add(mygame)
            # TODO : MAY CHANGE IN THE FUTURE
            db.session.commit()


    with ThreadPoolExecutor() as executor:
        query = f'SELECT game_id ,price ,developer ,discount_percent ,image , genres ,game_name ,review_negative ,short_description,review_positive FROM game WHERE game_name LIKE "%{game_name}%"'
   
        future = executor.submit(fetch_games,query, db.engine)
        df = future.result()
        # print(df)
    # print(df)
    if df == "Game not found":
      err = format_game_flex("error")
      out = custompayload(err)
      return jsonify(out) , 200
  
    games = format_game_detail_flex(df)
    # print(games)
    out = custompayload(games)
    
    return jsonify(out) , 200

def fetch_games(query, engine):
    # query = f'SELECT game_id ,price ,developer ,discount_percent ,image , genres ,game_name ,review_negative ,short_description,review_positive FROM game WHERE genres LIKE "%{genre}%"'
              
    df = pd.read_sql_query(query, engine)
    
    if df.empty:
      # TODO: CHANGE RETURN TO RETURN A CUSTOM PAYLOAD WITH MESSAGE
      
      return "Game not found"
    
    games = df.to_dict(orient='records')
    
    shuffle(games)
    return games

@bp.route('/export_game_date', methods=['GET'])
def export_game_date():

    df = pd.read_sql_query('SELECT * FROM game',db.engine)
    #df to csv
    df.to_csv('game.csv', index=False)
    
    return "SUCCESS EXPORT" , 200
@bp.route("/import_game_data", methods=["GET"])
def import_game_data():
    #drop every instance in game table
    db.session.query(Game).delete()
    db.session.commit()
    
    
    # Create a SQLAlchemy engine
    df = pd.read_csv('game.csv')

    # Insert DataFrame into the SQLite database
    df.to_sql('game', con=db.engine, if_exists='append', index=False)
    return "SUCCESS IMPORT" , 200