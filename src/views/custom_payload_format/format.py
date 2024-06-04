import datetime


def format_game_detail_flexs(item): 
 return {
  "type": "bubble",
  "size": "hecto",
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
              "label": "เพิ่มใส่รถเข็น",
              "data": "addCart "+str(item['game_id']),
              "displayText": "เพิ่ม "+str(item['game_name'])+" ใส่รถเข็น"
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
  # print(item)
  return {
  "type": "bubble",
  "size": "deca",
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
          "displayText": "ดูเกมแนว "+item,
        },
        "style": "primary",
        "margin": "xs",
        
      }
    ]
  }
}
    

# TODO : CHANGE TO DYNAMIC GAME DETAIL    
def format_cart(data,promotion):
    mylist = []
    def clean_price(price):
      # Remove the currency symbol and commas
      return float(price.replace(',', '').replace('฿', '').strip())
    total_price = sum(clean_price(item['price']) * item['game_quantity'] for item in data)

    total_quantity = 0
    for item in data:
        total_quantity += int(item['game_quantity'])
        # total_price += item['price']
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
                "text": "฿"+str(clean_price(item['price'])*int(item['game_quantity'])),
                "size": "sm",
                "align": "end",
   
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
        },)
    bubble = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "CART",
                        "weight": "bold",
                        "size": "md",
                        "color": "#1DB446"
                    },
                    {
                      "type": "text",
                      "text": "Laro Store",
                      "weight": "bold",
                      "size": "xxl",
                      "margin": "md"
                    },
                    {
                      "type": "separator",
                      "margin": "xxl"
                    },
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
                  "type": "separator",
                  "margin": "xxl"
                },
                {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "จำนวน",
                "size": "sm",
              },
              {
                "type": "text",
                "text": str(total_quantity),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "รวมค่าเกม",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "฿"+str(total_price),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "โปรโมชั่น",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "-"+str(promotion),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "รวมทั้งหมด",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "฿"+str(total_price-promotion),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
                {
                  "type": "separator",
                  "margin": "xxl"
                },
                {
                  
                  "type": "button",
                  "color": "#FF0000",
                  "action": {
                      "type": "postback",
                      
                      "label": "เคลียรถเข็น",
                      "data": "เคลียรถเข็น",
                      "displayText": "เคลียรถเข็น",
                  },
                  "style": "primary"
                },
                                {
                  "type": "separator",
                  "margin": "sm"
                },
                {
                  
                  "type": "button",
                  "action": {
                      "type": "postback",
                      "label": "สั่งสินค้า",
                      "data": "สั่งสินค้า",
                      "displayText": "สั่งสินค้า",
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
    # bubblelist.append( format_game_flexs(genre))
    for item in data:
        if(item['price'] == None or item['price'] == "" or item['price'] == "N/A" or item['price'] == "ฟรี"):
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
  
def promotion_payload_format(promotion):
  return {
  "type": "bubble",
  "size": "deca",
  "hero": {
    "type": "image",
    "url": "https://cdn-icons-png.flaticon.com/512/2037/2037266.png",
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
        "text": "โปรโมชั่น",
        "size": "xl",
        "wrap": True,
        "weight": "bold"
      },
      {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "contents": [

              {
                "type": "text",
                "text": "🏁ใช้ได้สูงสุด "+str(promotion['usage_limit'])+" ครั้ง",
                "weight": "bold",
                "margin": "sm",
                "flex": 0
              },

            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [

              {
                "type": "text",
                "text": "โปรจบในวันที่ "+promotion['end_date'].split("-")[2].split(" ")[0]+"/"+promotion['end_date'].split("-")[1],
                "weight": "bold",
                "margin": "sm",
                "flex": 0
              },

            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [

              {
                "type": "text",
                "text": "ขั้นต่ำ "+str(promotion['min_purchase'])+" บาท",
                "weight": "bold",
                "margin": "sm",
                "flex": 0
              },

            ]
          },
          

        ]
      },
      {
        "type": "text",
        "text": promotion['promotion_name'],
        "wrap": True,
        "color": "#aaaaaa",
        "size": "sm"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "color": "#905c44",
        "margin": "sm",
        "action": {
          "type": "postback",
          "label": "ใช้โปรโมชั่น",
          "data": "promotion "+ str(promotion['promotion_id']),
          "displayText": "ใช้โปรโมชั่น "+ str(promotion['promotion_name'])
        }
      }
    ]
  }
}
def error_payload_format(message):
  return custompayload({
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
              },
              
              {
                "type": "text",
                "contents": [],
                "size": "lg",
                "text": message,
                "color": "#ffffff",
                "weight": "bold",
                "margin": "none",
                "align": "center",
                "wrap": True
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
})
def success_payload_format(topic,message):
  return custompayload({
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
            "url": "https://cdn-icons-png.flaticon.com/512/7518/7518748.png",
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
                "text": "✅✅"+topic+"✅✅",
                "color": "#ffffff",
                "weight": "bold",
                "margin": "none",
                "align": "center"
              },
              
              {
                "type": "text",
                "contents": [],
                "size": "lg",
                "text": message,
                "color": "#ffffff",
                "weight": "bold",
                "margin": "none",
                "align": "start",
                "wrap": True
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
})
  
  
  
  
def order_payload_format(data):
    mylist = []
    def clean_price(price):
      # print(price)
      # Remove the currency symbol and commas
      return float(price.replace(',', '').replace('฿', '').strip())
    total_price = sum(clean_price(item['price_when_ordered']) * int(item['game_quantity']) for item in data)
    
    total_quantity = 0
    for item in data:
        total_quantity += int(item['game_quantity'])
        # total_price += item['price']
        mylist.append({
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": str(item['game_quantity'])+" "+str(item['game_name']),
                "size": "sm",
                "align": "start",
         
              }
               ,
              {
                "type": "text",
                "text": str(item['price_when_ordered']),
                "size": "sm",
                "align": "end",
   
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
        },)


    bubble = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "ORDER #"+str(data[0]['order_id']),
                        "weight": "bold",
                        "size": "md",
                        "color": "#1DB446"
                    },
                    {
                      "type": "text",
                      "text": "Laro Store",
                      "weight": "bold",
                      "size": "xxl",
                      "margin": "md"
                    },
                    {
                      "type": "separator",
                      "margin": "xxl"
                    },
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
                  "type": "separator",
                  "margin": "xxl"
                },
                {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "จำนวน",
                "size": "sm",
              },
              {
                "type": "text",
                "text": str(total_quantity),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "รวมค่าเกม",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "฿"+str(total_price),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "โปรโมชั่น",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "-"+str(item['discount']),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "รวมทั้งหมด",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "฿"+str(item['total_cost']-item['discount']),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "สถานะ",
                "size": "sm",
              },
              {
                "type": "text",
                "text": str(data[0]['order_status']),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
      {
                  "type": "separator",
                  "margin": "xxl"
                },
                {
                  
                  "type": "button",
                  "color": "#FF0000",
                  "action": {
                      "type": "postback",
                      
                      "label": "ยกเลิกคำสั่งซิ้อ",
                      "data": "cancel "+str(data[0]['order_id']),
                      "displayText": "ยกเลิกคำสั่งซิ้อ",
                  },
                  "style": "primary"
                },
                {
                  "type": "separator",
                  "margin": "sm"
                },
                {
                  
                  "type": "button",
                  "action": {
                      "type": "postback",
                      "label": "จ่ายเงิน",
                      "data": "จ่ายเงิน",
                      "displayText": "จ่ายเงิน",
                  },
                  "style": "primary"
                }
              ]
            },
        }
    return bubble
  
  
def his_order_payload_format(data):
    mylist = []
    def clean_price(price):
      # print(price)
      # Remove the currency symbol and commas
      return float(price.replace(',', '').replace('฿', '').strip())
    total_price = sum(clean_price(item['price_when_ordered']) * int(item['game_quantity']) for item in data)
    
    total_quantity = 0
    for item in data:
        total_quantity += int(item['game_quantity'])
        # total_price += item['price']
        mylist.append({
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": str(item['game_quantity'])+" "+str(item['game_name']),
                "size": "sm",
                "align": "start",
         
              }
               ,
              {
                "type": "text",
                "text": str(item['price_when_ordered']),
                "size": "sm",
                "align": "end",
   
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
        },)


    bubble = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "ORDER #"+str(data[0]['order_id']),
                        "weight": "bold",
                        "size": "md",
                        "color": "#1DB446"
                    },
                    {
                      "type": "text",
                      "text": "Laro Store",
                      "weight": "bold",
                      "size": "xxl",
                      "margin": "md"
                    },
                    {
                      "type": "separator",
                      "margin": "xxl"
                    },
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
                  "type": "separator",
                  "margin": "xxl"
                },
                {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "จำนวน",
                "size": "sm",
              },
              {
                "type": "text",
                "text": str(total_quantity),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "รวมค่าเกม",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "฿"+str(total_price),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "โปรโมชั่น",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "-"+str(item['discount']),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "รวมทั้งหมด",
                "size": "sm",
              },
              {
                "type": "text",
                "text": "฿"+str(item['total_cost']-item['discount']),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },
            
            {
            "type": "box",
            "layout": "horizontal",
            "contents":
              [
              {
                "type": "text",
                "text": "สถานะ",
                "size": "sm",
              },
              {
                "type": "text",
                "text": str(data[0]['order_status']),
                "size": "sm",
                "align": "end",
              }
            ],
            "margin": "none",
            "offsetEnd": "none",
            },

              ]
            },
        }
    return bubble
  
  
