def format_game_detail_flexs(item): 
 return {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": item['image'],
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": item['game_name'],
        "weight": "bold",
        "gravity": "center",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": item['developer'],
            "weight": "bold",
            "gravity": "center",
            "size": "md"
          },
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Reviews",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "Positive : "+str(item['review_positive']),
                "size": "sm",
                "weight": "bold",
                "color": "#009933",
                "flex": 4
              }
            ]
          },
                    {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Reviews",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "Negative : "+str(item['review_negative']),
                "size": "sm",
                "weight": "bold",
                "color": "#FF0000",
                "flex": 4
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Price ",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": str(item['price']),
                "color": "#000000",
                "weight": "bold",
                "size": "sm",
                "flex": 4
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Disc.(%)",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": str(item['discount_percent']), 
                "color": "#666666",
                "size": "sm",
                "flex": 4
              }
            ]
          },
    
                
              
      {
        
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "เพิ่มใส่ตะกร้า",
              "data": "addCart "+str(item['game_id']),
              "displayText": "เพิ่ม "+str(item['game_name'])+" ใส่ตะกร้า"
            },
            "style": "primary"
          }
        ]
      }
        ]
      },
    ]
  }
}
 
def format_game_flexs(item):
  print(item)
  return {
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
          "type": "postback",
          "label": "เลือกดูแนวเกม",
          "data": "ดูเกมแนว "+item,
          "displayText": "ดูเกมแนว "+item
        },
        "style": "primary",
        "margin": "xs",
        "offsetEnd": "none",
        "offsetTop": "none"
      }
    ]
  }
}
    

# TODO : CHANGE TO DYNAMIC GAME DETAIL    
def format_cart(data):
    mylist = []
    total_price = ''
    for item in data:
        total_price += item['price']
        mylist.append({
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": str(item['game_quantity'])+"   "+item['game_name'],
                "size": "sm",
         
              }
               ,
              {
                "type": "text",
                "text": str(item['price']*item['game_quantity']),
                "size": "sm",
                "align": "end",
   
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
        },)
    bubble = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Cart รถเข็น",
                        "weight": "bold",
                        "size": "md",
                        "color": "#1DB446"
                    }
                ],
                "margin": "none",
                "offsetEnd": "none"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": mylist,
            },
            "footer": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "uri",
                    "label": "Check Payment",
                    "uri": "http://linecorp.com/"
                  },
                  "style": "primary"
                }
              ]
            },
        }
    return bubble
  
def format_game_flex(data):
    bubblelist = []
    for item in data:
        if item == "เล่นฟรี" or item is None or item == "":
          continue
        bubblelist.append(format_game_flexs(item))
        
    carousel = {
        "type" : "carousel",
        "contents" : bubblelist[:10]
    }
    return carousel
        
def custompayload(flexdata):
  
    out = {
        "response_type" : "object" ,
        "line_payload" : [{
            "type" : "flex",
            "altText" : "Flex Message",
            "contents" : flexdata
        }]        
    }
    
    return out
  
  
def format_game_detail_flex(data):
    bubblelist = []
    
    for item in data:
        if(item['price'] == None or item['price'] == "" or item['price'] == "N/A"):
            item['price'] = "ไม่พบราคา"
            continue
        if(item['image'] == None or item['image'] == "" or item['image'] == " "):
            item['image'] = "https://th.bing.com/th/id/OIP.vDf037OKUo0H03weRxdWuAHaHa?rs=1&pid=ImgDetMain"
        if(item['discount_percent'] == None or item['discount_percent'] == "" or item['discount_percent'] == " " or item['discount_percent'] == "N/A"):
            item['discount_percent'] = "ไม่ลดราคา"
            
        bubblelist.append( format_game_detail_flexs (item))
        
    carousel = {
        "type" : "carousel",
        "contents" : bubblelist[:10]
    }
    
    return carousel
  
def promotion_payload_format(data):
#    https://cdn-icons-png.flaticon.com/512/2037/2037266.png 
    return {
        "type": "bubble",

    }
def error_payload_format():
  # https://cdn-icons-png.flaticon.com/512/8731/8731451.png
  return {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "image",
            "url": "https://cdn-icons-png.flaticon.com/512/8731/8731451.png",
            "size": "xxl",
            "aspectMode": "cover",
            "flex": 1
          }
        ]
      }
    ],
    "paddingAll": "0px"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "contents": [],
                "size": "lg",
                "text": "❌❌เกิดข้อผิดพลาด❌❌",
                "color": "#ffffff",
                "weight": "bold",
                "margin": "none",
                "align": "center"
              }
            ],
            "spacing": "sm"
          }
        ]
      }
    ],
    "paddingAll": "20px",
    "backgroundColor": "#464F69"
  }
}