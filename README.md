# Pac-Man
Версия 1.1

Автор: Щербина Евгений


## Описание

Данное приложение является реализацией игры «Pac-Man»
## Требования

- Python версии не ниже 3.6

- Pygame
## Состав

- Тесты: tests/

- Модули: .../

- Графическая версия: Pac-Man.py
## Консольная версия


- Справка по запуску: ./Pac-Man.py -h

- Пример запуска: ./Pac-Man.py
## Подробности реализации
...
/*
def text1(word,x,y):
    font = pygame.font.SysFont(None, 25)
    text = font.render("{}".format(word), True, (255,255,255))
    return screen.blit(text,(x,y))

def inpt():
    word=""
    text1("Please enter your name: ",300,400)
    pygame.display.flip()
    done = True
    while done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    done=False
                elif event.key == pygame.K_BACKSPACE:
                    word = word[:-1]
                else:
                    word += chr(event.key)
            screen.blit(img_Background, (0, 0))
            text1("Please enter your name: ", 300, 400)
            text1(word,300,450)
            pygame.display.flip()
    print(word)
    */
    /*
        def getplayername(self):
        try:
            import wx
        except:
            print("Pacman Error: No module wx. Can not ask the user his name!")
            print("     :(       Download wx from http://www.wxpython.org/")
            print("     :(       To avoid seeing this error again, set NO_WX in file pacman.pyw.")
            sys.exit(-1)
        app = wx.App(None)
        dlog = wx.TextEntryDialog(None, "You made the high-score list! Name:")
        dlog.ShowModal()
        name = dlog.GetValue()
        dlog.Destroy()
        app.Destroy()
        return name
      */
