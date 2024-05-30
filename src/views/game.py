from concurrent.futures import ThreadPoolExecutor
import json
from flask import Blueprint, jsonify , request
from random import shuffle
from ..models import db
import pandas as pd
from .custom_payload_format.format import custompayload, format_game_detail_flex, format_game_detail_flexs, format_game_flex, format_game_flexs

bp = Blueprint("game", __name__, url_prefix="/game")

@bp.route("/genre", methods=["GET"])
def get_game_genre():

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
    query = f'SELECT game_id ,game_name FROM gamelist WHERE game_name LIKE "%{game_name}%"'

    # TODO : IMPLEMENT INTO THREAD
    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(fetch_games, query, db.engine)
    # df = pd.read_sql_query(query, db.engine)
    # print(future.result())
    # if df.empty:
        # TODO: CHANGE RETURN TO RETURN A CUSTOM PAYLOAD WITH MESSAGE
        # return "Game not found"
    
    # games = df.to_dict(orient='records')
    # shuffle(games)
    return jsonify(future.result()), 200

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
@bp.route("/import_game_date", methods=["GET"])
def import_game_data():
    

    # Create a SQLAlchemy engine
    df = pd.read_csv('game.csv')

    # Insert DataFrame into the SQLite database
    df.to_sql('game', con=db.engine, if_exists='append', index=False)
    return "SUCCESS IMPORT" , 200