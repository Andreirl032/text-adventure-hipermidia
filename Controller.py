import Model as m
import View as v
import Player as p

class Controller:
    def __init__(self):
        self.currLocation=None
        self.commands=["ajuda","ir","ver","pegar","perfil"]
        self.difficulty="" #a dificuldade pode ser "fácil", "normal", ou "difícil"
        self.state="" #o estado pode ser "exploration", "combat", "talk", ou "puzzle"
        self.player=None

    def playGame(self):
        gameInfo=m.Model()
        view=v.View()
        self.currLocation=gameInfo.startLocationId
        self.player=p.Player(gameInfo.attack,gameInfo.defense,gameInfo.life,gameInfo.maxItems)
        view.beginGame(self,gameInfo)

    def findCurrLocation(self,gameInfo):
        for i in gameInfo.locations:
            if i["id"]==self.currLocation:
                return i
        return {}
    
    def processCommand(self,command,gameInfo):
        if(command=="perfil"):
            self.verPerfil(gameInfo)
    
    def verPerfil(self,gameInfo):
        print("SUAS INFORMAÇÕES")
        print("HP: "+self.player.life+"/"+gameInfo.life)
        print("Ataque: "+self.player.attack)
        print("Defesa: "+self.player.defense)
        print(f"Itens ({len(self.player.items)}/{self.player.maxItems}): ")
        if(len(self.player.items)<1):
            print("sem itens")
        else:
            for i in self.player.items:
                print(i)

