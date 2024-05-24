import json
from flask import Blueprint, jsonify , request
from random import shuffle
from ..models import db
import pandas as pd

bp = Blueprint("game", __name__, url_prefix="/game")

@bp.route("/genre", methods=["GET"])
def get_game_genre():

    df = pd.read_sql_query('SELECT * FROM games',db.engine)
    df['genre_split'] = df['genre'].str.split(', ')
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
    
    genre = request.args.get("genre")
    าฃ
    df = pd.read_sql_query('SELECT * FROM games WHERE genre LIKE "%'+genre+'%"',db.engine)
    games = df.to_dict(orient='records')
    print(games)
    
    game_carousel = format_game_flex(games)
    out = custompayload(game_carousel)
    # print(df)
    #TODO: MAKE IT COUROUSEL 
    return jsonify(out) , 200


def format_game_flex(data):
    bubblelist = []
    for item in data:

        bubblelist.append({
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Genre แนวเกม",
        "weight": "bold",
        "size": "md",
        "color": "#1DB446"
      },
      {
        "type": "text",
        "text": item,
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
      }
    ],
    "margin": "none",
    "offsetEnd": "none"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "เลือกดูเกม",
          "text": "ดูเกมแนว "+item
        },
        "style": "primary",
        "margin": "xs",
        "offsetEnd": "none",
        "offsetTop": "none"
      }
    ]
  }
})
        
    carousel = {
        "type" : "carousel",
        "contents" : bubblelist[:10]
    }
    # print(carousel)
    # print(bubblelist)
    return carousel
        
def custompayload(flexdata):
    out = {
        "response_type" : "object" ,
        "line_payload" : [{
            "type" : "flex",
            "altText" : "แนวเกม",
            "contents" : flexdata
        }]        
    }
    return out
