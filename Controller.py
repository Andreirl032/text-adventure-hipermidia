import Model as m
import Player as p
import View as v
class Controller:
    def __init__(self):
        self.currLocation=None
        self.commands=["ajuda",""]
        self.difficulty="" #a dificuldade pode ser "fácil", "normal", ou "difícil"
        self.state="" #o estado pode ser "exploration", "combat", ou "puzzle"
        self.player=None

    def playGame(self):
        gameInfo=m.Model()
        view=v.View()
        self.currLocation=gameInfo.startLocationId
        self.player=p.Player(gameInfo.attack,gameInfo.defense,gameInfo.life,gameInfo.maxItems)
        self.difficulty=view.beginGame(gameInfo.title,gameInfo.author,gameInfo.description,self.currLocation,self.player,self.commands)
