import json
with open('game.json', 'r') as file:
    data = json.load(file)

class Model:
    def __init__(self):
        self.title=data["title"]
        self.description=data["description"]
        self.author=data["author"]
        self.startLocationId=data["startLocationId"]
        self.maxItems=data["maxItems"]
        self.attack=data["attack"]
        self.defense=data["defense"]
        self.life=data["life"]
        self.locations=data["locations"]