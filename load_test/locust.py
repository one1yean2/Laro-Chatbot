import json
from locust import HttpUser, task, between
import random

class GameBehavior(HttpUser):
    wait_time = between(1, 5)
    customer_id = str(random.randint(1, 1000))

    @task
    def get_game_genre(self):
        self.client.get(f"/game/genre?customer_id={self.customer_id}")

    @task
    def get_games_from_genre(self):
        genres = ["ดูเกมแนว แคชชวล", "ดูเกมแนว แอ็คชัน", "ดูเกมแนว ผู้เล่นหลายคน", "ดูเกมแนว กีฬา"]
        genre = random.choice(genres)
        self.client.get(f"/game/?customer_id={self.customer_id}&genre={genre}")

    @task
    def search_game(self):
        game_names = ["Zomboid", "Cyberpunk", "Stardew Valley", "Hades", "Terraria"]
        game_name = random.choice(game_names)
        self.client.get(f"/game/search?customer_id={self.customer_id}&game_name={game_name}")

    @task
    def add_to_cart(self):
        customer_id = random.randint(1, 1000)
        game_ids = ["addCart 1623730","addCart 1938090","addCart 553850","addCart 1086940"]
        game_id = random.choice(game_ids)
        self.client.post("/cart/add_to_cart", json={
            "customer_id": customer_id,
            "game_id": f"{game_id}"
        })
        self.client.get("/cart/view_cart", params={"customer_id": customer_id})
        self.client.post("/cart/clear_cart", json={"customer_id": customer_id})
    # @task
    # def view_cart(self):
    #     customer_id = random.randint(1, 1000)
    #     self.client.get("/cart/view_cart", params={"customer_id": customer_id})
        
    # @task
    # def clear_cart(self):
    #     customer_id = random.randint(1, 1000)
    #     self.client.post("/cart/clear_cart", json={"customer_id": customer_id})
        
        
    @task
    def get_promotion(self):
        customer_id = random.randint(1, 1000) # Replace with your customer ID or use a random generator
        response = self.client.get(f"/promotion/get_promotion?customer_id={customer_id}")
        if response.status_code == 200:
            print("Promotions retrieved successfully")
        else:
            print("Error retrieving promotions")

    @task
    def use_promotion(self):
        customer_id = random.randint(1, 1000)  # Replace with your customer ID or use a random generator
        data = {"customer_id": customer_id, "promotion_id": "promo 1"}  # Replace promotion_id with an actual promotion ID
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/promotion/use_promotion", data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Promotion used successfully")
        else:
            print("Error using promotion")

    @task
    def discard_promotion(self):
        customer_id = random.randint(1, 1000)  # Replace with your customer ID or use a random generator
        response = self.client.get(f"/promotion/discard_promotion?customer_id={customer_id}")
        if response.status_code == 200:
            print("Promotion discarded successfully")
        else:
            print("Error discarding promotion")
            
    @task
    def edit_profile(self):
        customer_id = random.randint(1, 1000)   # Replace with your customer ID or use a random generator
        email = "test@example.com"  # Replace with the email you want to set
        data = {"customer_id": customer_id, "email": email}
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/user/edit_profile", data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Profile edited successfully")
        else:
            print("Error editing profile")

    @task
    def get_info(self):
        customer_id = random.randint(1, 1000)   # Replace with your customer ID or use a random generator
        response = self.client.get(f"/user/get_info?customer_id={customer_id}")
        if response.status_code == 200:
            print("Info retrieved successfully")
        else:
            print("Error retrieving info")