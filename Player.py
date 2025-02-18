class Player:
    def __init__(self,attack,defense,life,maxItems):
        self.attack=attack
        self.defense=defense
        self.life=life
        self.maxItems=maxItems
        self.items=[]
        self.armor=None
