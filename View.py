import Model
import platform

if(platform.system()=="Windows"):
    import winsound

class View:
    def __init__(self):
        pass

    def gameLoop(controller,gameInfo):
        if(platform.system()=="Windows"):
            winsound.PlaySound(r'./exploration.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
        while(controller.player.life>0):
            infoCurrLocation=controller.findCurrLocation(gameInfo)
            print("--------------------"+infoCurrLocation["name"]+"--------------------")
            print(infoCurrLocation["description"])
            command="input"
            if(command in controller.commands):
                controller.processCommand(command,gameInfo)

    def beginGame(self,controller,gameInfo):
        print("--------------------"+gameInfo.title+"--------------------")
        print("Feito por "+gameInfo.author)
        print(gameInfo.description+"\n")
        while(True):
            enter=int(input("ESCOLHA A DIFICULDADE:\n1-FÁCIL\n2-NORMAL\n3-DIFÍCIL\n"))
            dificuldade=["fácil","normal","difícil"]
            if(enter>0 and enter<4):
                controller.difficulty=dificuldade[enter-1]
                View.gameLoop(controller,gameInfo)
                return
            else:
                print("INSIRA UM NÚMERO VÁLIDO")