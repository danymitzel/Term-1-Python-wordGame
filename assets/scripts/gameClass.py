import os.path
from threading import Thread

from assets.scripts.settings import *


class Game():
    def __init__(self):
        pg.mixer.init()
        self.root = Tk()
        self.load_imgs()
        self.load_music()
        self.root_setup()

        self.file = self.open_file(os.path.join(self.wordBank_folder,"wordlist.txt"),"r")
        self.wordBank = self.read_in_data(self.file)

        self.cur_bg_color = bg_color
        self.cur_correct_color = correct_color
        self.cur_close_color = close_color
        self.cur_wrong_color = wrong_color
        self.cur_accent_color = accent_color
        self.cur_font_color = font_color

        self.create_title()

        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.5)


#setup methods#
    def open_file(self,filename,per):
        try:
            open_file_obj = open(filename,per)
            return open_file_obj
        except:
            print("had an error")

    def read_in_data(self,file):
        temp_list = file.readlines()
        word_list = []

        for word in temp_list:
            x=word.replace("\n","").upper()
            word_list.append(x)


        return word_list



        temp = file.readlines()
        cleanList = []
        for item in temp:
            cleanList.append(item.replace("\n",""))



    def load_imgs(self):
        self.file_location = os.path.dirname(__file__)
        self.file_location = self.file_location.replace("\\assets\\scripts", "")
        self.assets_folder = os.path.join(self.file_location, "assets")
        self.sprites_folder = os.path.join(self.assets_folder, "sprites")
        self.scripts_folder = os.path.join(self.assets_folder, "scripts")
        self.sounds_folder = os.path.join(self.assets_folder, "sounds")
        self.wordBank_folder = os.path.join(self.assets_folder, "wordbank")
        self.icon_img = os.path.join(self.sprites_folder, "IconImage.ico")
        self.title_img_name = os.path.join(self.sprites_folder, "wordddle.png")
        self.title_img = PhotoImage(file=self.title_img_name)
        self.rules_img = os.path.join(self.sprites_folder,"rules.png")
        self.rules_img = PhotoImage(file=self.rules_img)

    def load_music(self):
        pg.mixer.music.load(os.path.join(self.sounds_folder, "Background_Music.mp3"))
        self.bttn_click = pg.mixer.Sound(os.path.join(self.sounds_folder, "clickbuttn.mp3"))
        self.win_snd = pg.mixer.Sound(os.path.join(self.sounds_folder, "youwin.mp3"))
        self.lose_snd = pg.mixer.Sound(os.path.join(self.sounds_folder, "fail8bit.mp3"))


    #scene set up messages
    def create_title(self):
        #this section of code is to create the title screen#
        self.title_screen = Frame(self.root,width=self.root.winfo_width(),height=self.root.winfo_height(),background=self.cur_bg_color)
        self.gameTitle = Label(self.title_screen,text = TITLE,background=self.cur_bg_color,foreground=self.cur_font_color ,font="arial 100 bold")
        self.gameTitle.place(x=self.root.winfo_width()/2,y=120,anchor=CENTER)
        Label(self.title_screen,image=self.title_img,justify=CENTER).place(x=self.root.winfo_width()/2,y=self.root.winfo_height()/2,anchor=CENTER)
        Button(self.title_screen,text="Play Game",command=self.start_game,font="arial 25",width=15).place(x=self.root.winfo_width()/2,y=820,anchor=CENTER)
        Button(self.title_screen, text="Rules", command=self.start_rules, font="arial 25", width=15).place(x=self.root.winfo_width() / 2, y=920, anchor=CENTER)
        self.title_screen.pack(expand=True,fill=BOTH)

    def create_rules(self):
        self.rules_screen = Frame(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(),background=self.cur_bg_color)
        self.rulesTitle = Label(self.rules_screen, text="Wordle", background=self.cur_bg_color, foreground=self.cur_font_color, font="arial 100 bold")
        self.rulesTitle.place(x=self.root.winfo_width() / 2, y=120, anchor=CENTER)
        Label(self.rules_screen, image=self.rules_img, justify=CENTER).place(x=self.root.winfo_width() / 2,y=self.root.winfo_height() / 2,anchor=CENTER)
        Button(self.rules_screen, text="Back", command=self.back_to_title, font="arial 25", width=15).place(x=self.root.winfo_width() / 2, y=820, anchor=CENTER)
        self.rules_screen.pack(expand=True, fill=BOTH)


    def create_game(self):
        #this method will create all of the game widgets needed to play the game and the scene #
        self.word = random.choice(self.wordBank)
        print(self.word)
        self.maxtrys = 6
        self.cur_letter = 0
        self.cur_try = 0
        self.board = []
        tileWidth = 75
        tileHeight = 100


        self.game_screen = Frame(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(),background=self.cur_bg_color)
        self.game_screen.rowconfigure(0,weight=2)
        self.game_screen.rowconfigure(1,weight=1)


        self.board_frame= Frame(self.game_screen,width=self.root.winfo_width(),background=self.cur_bg_color)
        self.timer = Label(self.board_frame,text="00:00",background=self.cur_bg_color,foreground=self.cur_font_color,font="Arial 25")
        self.timer.place(x=650,y=25)

        x = self.root.winfo_width()/2-(len(self.word) / 2 * tileWidth)
        y = 25
        for row in range(self.maxtrys):
            temp_list = []
            for col in range(len(self.word)):
                temp = Label(self.board_frame,text="",justify=CENTER,font="Arial 18",height=3,width=4,background=self.cur_accent_color,foreground=self.cur_font_color)
                temp_list.append(temp)
                temp.place(x=x,y=y)
                x+=tileWidth
            self.board.append(temp_list)
            y+=tileHeight
            x = self.root.winfo_width() / 2 - (len(self.word) / 2 * tileWidth)


        self.keyboard = Frame(self.game_screen,width=self.root.winfo_width(),background=self.cur_bg_color)
        self.keyboard_buttns = []
        row0 = "QWERTYUIOP"
        row1 = "ASDFGHJKL"
        row2 = "ZXCVBNM"
        tileWidth = 55
        tileHeight = 55

        x = self.root.winfo_width()/2 -(len(row0)/2*tileWidth)
        y = 40
        for i in range(len(row0)):
            temp = Button(self.keyboard,text=row0[i],width=3,font="Arial 18",background=self.cur_accent_color,foreground=self.cur_font_color,activebackground=self.cur_bg_color,
                          command = lambda id=i, letter = row0[i]:self.guessLetter(id,letter))
            temp.place(x=x,y=y)
            self.keyboard_buttns.append(temp)
            x += tileWidth

        x = self.root.winfo_width() / 2 - (len(row1) / 2 * tileWidth)
        y += tileHeight
        for i in range(len(row1)):
            temp = Button(self.keyboard, text=row1[i], width=3, font="Arial 18", background=self.cur_accent_color,
                          foreground=self.cur_font_color, activebackground=self.cur_bg_color, command= lambda id=i+len(row0), letter = row1[i]:self.guessLetter(id,letter))
            temp.place(x=x, y=y)
            self.keyboard_buttns.append(temp)
            x += tileWidth

        x = self.root.winfo_width() / 2 - (len(row2) / 2 * tileWidth)
        y += tileHeight
        for i in range(len(row2)):
            temp = Button(self.keyboard, text=row2[i], width=3, font="Arial 18", background=self.cur_accent_color,
                          foreground=self.cur_font_color, activebackground=self.cur_bg_color, command= lambda id=i+len(row1)+len(row0), letter = row2[i]:self.guessLetter(id,letter))
            temp.place(x=x, y=y)
            self.keyboard_buttns.append(temp)
            x += tileWidth
        self.bs_bttn = Button(self.keyboard,text="⌫",background=self.cur_accent_color,
                          foreground=self.cur_font_color, activebackground=self.cur_bg_color,width=5,height=1,font="Arial 18",command=self.backSpace )

        self.submit_bttn = Button(self.keyboard, text="↵", background=self.cur_accent_color,
                              foreground=self.cur_font_color, activebackground=self.cur_bg_color, width=5, height=1,
                              font="Arial 18", command=self.guessWord)
        self.submit_bttn.place(x=145,y=y)
        self.bs_bttn.place(x=615,y=y)


        for row in range(self.maxtrys):
            templist = []
            for col in range(len(self.word)):
                temp =Label(self.board_frame,text="",justify=CENTER)
                temp.place()
                templist.append(temp)



        self.board_frame.grid(row=0,column=0,sticky=NSEW)
        self.keyboard.grid(row=1,column=0,sticky=NSEW)
        self.game_screen.pack(expand=True, fill=BOTH)

        #add buttons to the keyboard
        # letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
        # self.bttn_list = []
        # col = 1
        # row = 0
        # id=0
        # for l in letters:
        #     temp = Button(self.keyboard,text =l, width=2,font="arial 10 bold",command=lambda id=id ,letter=l:self.pick_letter(id,letter))
        #     temp.grid(row=row,column=col,padx=5, pady=5, ipadx=5, ipady=5 )
        #     id+=1
        #     self.bttn_list.append(temp)
        #     col+=1
        #     if row==0 and col >10:
        #         row+=1
        #         col=2
        #     elif row==1 and col >10:
        #         row+=1
        #         col=3
        #
        #
        # # row 0
        # self.dif_selector.grid(row=0,column=0,sticky=NSEW,padx=5,pady=5,ipadx=5,ipady=5)
        # # row 1
        # self.display.grid(row=1,column=0,columnspan=3,sticky=NSEW,padx=5,pady=5,ipadx=5,ipady=5)
        # # row 2
        # self.letter_display.grid(row=2, column=0, columnspan=3, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
        # self.guess_bttn.grid(row=3, column=2, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
        #
        # # row 3
        # self.hint_bttn.grid(row=3, column=0, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
        # # row 4
        # self.word_entry.grid(row=4, column=0, columnspan=3, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
        #
        # # row 5
        # self.keyboard.grid(row=5,column=1,sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)

        Button(self.game_screen, text="quit", command=self.end_game).grid(row=6,column=0,columnspan=3,sticky=NSEW)


        self.game_screen.pack(expand=True, fill=BOTH)


    def create_end(self):

        self.end_screen = Frame(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(),background=self.cur_bg_color)
        self.gameOverMsg = Label(self.end_screen, text=self.end_msg, background=self.cur_bg_color, foreground="black",font="arial 100 bold")
        self.gameOverMsg.place(x=self.root.winfo_width() / 2, y=120, anchor=CENTER)
        Label(self.end_screen, text="The word was "+self.word,justify=CENTER, font="arial 25").place(x=self.root.winfo_width() / 2,y=self.root.winfo_height() / 2,anchor=CENTER)
        Button(self.end_screen, text="Back to Title", command=self.back_to_title, font="arial 25",width=15).place(x=self.root.winfo_width() / 2, y=820, anchor=CENTER)
        Button(self.end_screen, text="Quit", command=self.quit_game, font="arial 25",width=15).place(x=self.root.winfo_width() / 2, y=920, anchor=CENTER)
        self.end_screen.pack(expand=True, fill=BOTH)


#navigation methods
    def start_game(self):

        self.title_screen.destroy()
        self.create_game()

    def start_rules(self):
        self.bttn_click.play()
        self.title_screen.destroy()
        self.create_rules()


    def end_game(self):
        self.game_screen.destroy()
        self.create_end()


    def back_to_title(self):
        self.bttn_click.play()
        try:
            self.end_screen.destroy()
            self.create_title()
        except:
            pass
        try:
            self.rules_screen.destroy()
            self.create_title()
        except:
            pass

    def quit_game(self):
        self.root.destroy()

    def guessLetter(self,id,letter):
        if self.cur_letter < len(self.word):
            self.bttn_click.play()
            self.board[self.cur_try][self.cur_letter].config(text=letter)
            self.cur_letter +=1

    def guessWord(self):
        if self.cur_letter == len(self.word):
            newWord = ""
            for i in range(len(self.board[self.cur_try])):
                newWord+=self.board[self.cur_try][i]["text"]
            newWord = newWord.upper()
            self.word = self.word.upper()
            if newWord in self.wordBank:
                #ding sound if word in bank error sound if word not real
                correct_count = 0
                for i in range(len(self.board[self.cur_try])):
                    l = self.board [self.cur_try][i]["text"]
                    if l == self.word [i]:
                        self.board[self.cur_try][i].config(background=self.cur_correct_color)
                        correct_count+=1
                    elif l in self.word:
                        self.board[self.cur_try][i].config(background=self.cur_close_color)
                    else:
                        self.board[self.cur_try][i].config(background=self.cur_wrong_color)
                    for bttn in self.keyboard_buttns:
                        if bttn["text"]==l:
                            if l == self.word[i]:
                                bttn.config(background=self.cur_correct_color)
                            elif l in self.word:
                                bttn.config(background=self.cur_close_color)
                            else:
                                bttn.config(background=self.cur_wrong_color)

            else:
                #play error sound
                pass

            if correct_count == len(self.word):
                self.win_snd.play()
                self.win_lose(True)
            else:
                self.cur_letter = 0
                self.cur_try +=1
                if self.cur_try >= self.maxtrys:
                    self.lose_snd.play()
                    self.win_lose(False)


    def win_lose(self,win):
        self.end_msg = ""
        if win:
            self.win_snd.play()
            self.end_msg = "YOU WIN"
        else:
            self.lose_snd.play()
            self.end_msg = "YOU LOSE"
        self.end_game()





    def backSpace(self):
        if self.cur_letter >0:
            self.bttn_click.play()
            self.board[self.cur_try][self.cur_letter-1].config(text="")
            self.cur_letter += -1



    #set up messages#

    def root_setup(self):
        self.root.geometry(geoString)
        self.root.title(TITLE)
        self.root.iconbitmap(self.icon_img)
        self.root.resizable(0,0)

    def play(self):

        self.root.mainloop()
#action methods#
    def update_color(self):
        self.title_screen.config(background=self.cur_bg_color)
        self.gameTitle.config(background=self.cur_bg_color,foreground=self.cur_font_color)
        self.rules_screen.config(background=self.cur_bg_color)
        self.rulesTitle.config(background=self.cur_bg_color, foreground=self.cur_font_color)
