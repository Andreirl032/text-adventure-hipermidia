import Model as m
import Player as p
import View as v
class Controller:
    def __init__(self):
        self.currLocation=None

    def playGame(self):
        gameInfo=m.Model()
        view=v.View()
        player=p.Player(gameInfo.attack,gameInfo.defense,gameInfo.life,gameInfo.maxItems)
        self.currLocation=gameInfo.startLocationId
