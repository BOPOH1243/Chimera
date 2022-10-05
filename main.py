import glowhack
from espbox import *
from tkinter import *
from triggerbot import TriggerBot

def main():
    cheats = []
    cheats.append(ESPBox())
    cheats.append(TriggerBot())
    win = Tk()
    win.title("Cheat client Chimera")
    win.geometry("500x600+10+10")
    win.resizable(False,False)
    photo = PhotoImage(file='icon.png')
    win.iconphoto(False,photo)
    for cheat in cheats:
        btn = Button(win, text=cheat.get_name(),command=cheat.start)
        btnstop = Button(win,text=f'{cheat.get_name()} stop',command=cheat.stop)
        btnstop.pack()
        btn.pack()

    win.mainloop()

if __name__ == '__main__':
    main()