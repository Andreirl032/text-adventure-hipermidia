import Model
import winsound

class View:
    def __init__(self):
        pass

    def gameLoop(currSpace,currPlayer,commands):
        winsound.PlaySound(r'./exploration.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
        b=0
        while(currPlayer.life>0 and b<1):
            a=input("oie\n")
            b+=1
            pass
        print("oi")
        pass

    def beginGame(self,title,author,desc,currSpace,currPlayer,commands):
        print("--------------------"+title+"--------------------")
        print("Feito por "+author)
        print(desc+"\n")
        while(True):
            enter=int(input("ESCOLHA A DIFICULDADE:\n1-FÁCIL\n2-NORMAL\n3-DIFÍCIL\n"))
            dificuldade=["fácil","normal","difícil"]
            if(enter>0 and enter<4):
                View.gameLoop(currSpace,currPlayer,commands)
                return dificuldade[enter-1]
            else:
                print("INSIRA UM NÚMERO VÁLIDO")