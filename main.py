# All the imports needed

# Imports for Spotipy
import spotipy # Spotify web API wrapper for python
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth # Auth
from spotipy.oauth2 import SpotifyClientCredentials # Auth

# Imports for GUI
from tkinter import *
import tkinter.ttk as ttk

# Imports for audio playback
import time
import vlc

# OTHER
import sys
import random
import mysql.connector
# from os import popen


# Internal AUTH
auth_manager= SpotifyClientCredentials ( 
    client_id = 'd4249435a9b24617a534b2bd542c7437', 
    client_secret = '1db701fa67ee41209a1fee33c4df9088'
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# MySQL Connection
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "af034850",
    database= "song_guesser_game"
)
mycursor = db.cursor(buffered=True)
mycursor.execute("SELECT Username,Category,Score,Playlist_URL FROM scoreboard")

def initialize_database():
    mycursor.execute("SELECT Username,Category,Score,Playlist_URL FROM scoreboard")
    records = mycursor.fetchall()
    print(records)

    for i, (username,category,score,playlist_url) in enumerate(records, start=1):
        scoreboard_treeview.insert("", "end", values=(username,category,score,playlist_url))
        db.close()

    for col in cols:
        scoreboard_treeview.heading(col, text=col)    
        scoreboard_treeview.grid(row=1, column=0, columnspan=2)
    
    scoreboard_treeview.place(
    x = 100, y = 150
    )




# ARTIST NAME AND PREVIEW URL
all_artist_name = []
all_preview_url = []
artist_name = [] # only working artists' name
preview_url = [] # only working preview URLs

# GLOBAL VARIABLES
username_scoreboard = ""
category_scoreboard = ""
song_number = 0

contor = 0
def incrementContor():
    global contor
    contor = contor + 4

score = 0
def setScore():
    global score
    if guesses == 3:
        score += 30
    if guesses == 2:
        score += 20
    if guesses == 1:
        score += 10
    print("SCORE:",score)
    #set label
    rap_label5.config(text=score)
    pop_label5.config(text=score)
    rock_label5.config(text=score)
    custom_game_label5.config(text=score)

guesses = 3
def decrementGuesses():
    global guesses
    if guesses > 0:
        guesses = guesses - 1
    print("GUESSES DECREMENT:",guesses)
def resetGuesses():
    setScore()
    global guesses
    guesses = 3
    print("GUESSES RESET:",guesses)

random_list = list()
local_random_list = list()

# PREDEFINED PLAYLISTS
rap_playlist = "https://open.spotify.com/playlist/20KFlOY06jSEcv0Yq2qpzY?si=0ad3bb2052ef45dc"
pop_playlist = "https://open.spotify.com/playlist/2fr0SVhl5mNtoLSSZys3yh?si=98eaaf171e9a442d"
rock_playlist = "https://open.spotify.com/playlist/1lGMOVQUb1XZyhP8hUTzsc?si=6253110c0f8146ac"

# CUSTOM GAME PLAYLIST
custom_game_playlist = ""


# RANDOM DEF
def randomize_list():
    temp_list = list()
    len_playlist = len(artist_name)
    while(len_playlist%4 != 0):
        len_playlist -= 1
        print(len_playlist)
    for i in range(len_playlist):
        random_list.append(i+1)
    
    print("INTIAL LIST",random_list)
    random.shuffle(random_list)
    print("RANDOMIZE LIST:", random_list)

def randomize_local_list():
    local_random_list.clear()
    i = contor
    while(i <= contor+3):
        local_random_list.append(random_list[i])
        i += 1
    print("mini list:", local_random_list)
    incrementContor()


# GETTING DATA FROM PLAYLIST
def get_data(enter_playlist):
    playlist_id = enter_playlist[34 : 56]
    playlist_info = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
    playlist_length = len(playlist_info["tracks"]["items"])
    print(playlist_length)
    for i in range(playlist_length):
        all_artist_name.append(playlist_info["tracks"]["items"][i]["track"]["name"])
        all_preview_url.append(playlist_info["tracks"]["items"][i]["track"]["preview_url"])
        
        if all_preview_url[i] is not None:
            #print(all_artist_name[i])
            #print(all_preview_url[i])
            #print()
            artist_name.append(all_artist_name[i])
            preview_url.append(all_preview_url[i])
    print(len(artist_name))
    #print(len(all_preview_url))


# GUESS SONG NUMBER
def rap_guess_song():
    checker = int(rap_entry0.get())
    print(checker,song_number)
    print(contor)
    if checker == song_number:
        if contor+4 < len(artist_name):
            randomize_local_list()
            resetGuesses()
            rap_start()
            print("CONTOR:",contor)
            print("ARTIST_NAME:",len(artist_name))
        else:
            resetGuesses()
            global category_scoreboard
            category_scoreboard = "Rap"
            print("FOR SCOREBOARD:",username_scoreboard,category_scoreboard,score)
            
            mycursor.execute("INSERT INTO scoreboard (username,category,score) VALUES (%s,%s,%s)", (username_scoreboard, category_scoreboard, score))
            db.commit()
            
            initialize_database()
            scoreboard_frame.tkraise()
    else:
        decrementGuesses()

def pop_guess_song():
    checker = int(pop_entry0.get())
    print(checker,song_number)
    print(contor)
    if checker == song_number:
        if contor+4 < len(artist_name):
            randomize_local_list()
            resetGuesses()
            pop_start()
            print("CONTOR:",contor)
            print("ARTIST_NAME:",len(artist_name))
        else:
            resetGuesses()
            global category_scoreboard
            category_scoreboard = "Pop"
            print("FOR SCOREBOARD:",username_scoreboard,category_scoreboard,score)
            
            mycursor.execute("INSERT INTO scoreboard (username,category,score) VALUES (%s,%s,%s)", (username_scoreboard, category_scoreboard, score))
            db.commit()
            
            initialize_database()
            scoreboard_frame.tkraise()
    else:
        decrementGuesses()

def rock_guess_song():
    checker = int(rock_entry0.get())
    print(checker,song_number)
    print(contor)
    if checker == song_number:
        if contor+4 < len(artist_name):
            randomize_local_list()
            resetGuesses()
            rock_start()
            print("CONTOR:",contor)
            print("ARTIST_NAME:",len(artist_name))
        else:
            resetGuesses()
            global category_scoreboard
            category_scoreboard = "Rock"
            print("FOR SCOREBOARD:",username_scoreboard,category_scoreboard,score)
            
            mycursor.execute("INSERT INTO scoreboard (username,category,score) VALUES (%s,%s,%s)", (username_scoreboard, category_scoreboard, score))
            db.commit()
            
            initialize_database()
            scoreboard_frame.tkraise()
    else:
        decrementGuesses()

def custom_game_guess_song():
    checker = int(custom_game_entry0.get())
    print(checker,song_number)
    print(contor)
    if checker == song_number:
        if contor+4 < len(artist_name):
            randomize_local_list()
            resetGuesses()
            custom_game_start()
            print("CONTOR:",contor)
            print("ARTIST_NAME:",len(artist_name))
        else:
            resetGuesses()
            global category_scoreboard
            category_scoreboard = "Custom Game"
            print("FOR SCOREBOARD:",username_scoreboard,category_scoreboard,score)
            
            mycursor.execute("INSERT INTO scoreboard (username,category,score,playlist_url) VALUES (%s,%s,%s,%s)", (username_scoreboard, category_scoreboard, score, custom_game_playlist))
            db.commit()
            
            initialize_database()
            scoreboard_frame.tkraise()
    else:
        decrementGuesses()


# MUSIC START
def rap_start():
    print("LOCAL RANDOM LIST:", local_random_list)
    for k in range(len(local_random_list)):
        print(preview_url[local_random_list[k]])
    
    rap_label1.config(text=artist_name[local_random_list[0]])
    rap_label2.config(text=artist_name[local_random_list[1]])
    rap_label3.config(text=artist_name[local_random_list[2]])
    rap_label4.config(text=artist_name[local_random_list[3]])

    random_number = random.randrange(1,5)
    print(random_number)

    player = vlc.MediaPlayer(preview_url[local_random_list[random_number-1]])
    player.audio_set_volume(50)
    print("Playing!",)
    player.play()

    time_spent = 0
    total_time = 5
    while(time_spent<total_time):
        time.sleep(0.05)
        rap_bar['value'] += 0.99
        window.update_idletasks()
        rap_frame.update()
        #print(time_spent)
        time_spent += 0.05
    rap_bar['value'] = 0

    player.stop()
    print("PLAYED SONG NUMBER:",random_number)
    global song_number
    song_number = random_number
    print(song_number)

def pop_start():
    print("LOCAL RANDOM LIST:", local_random_list)
    for k in range(len(local_random_list)):
        print(preview_url[local_random_list[k]])
    
    pop_label1.config(text=artist_name[local_random_list[0]])
    pop_label2.config(text=artist_name[local_random_list[1]])
    pop_label3.config(text=artist_name[local_random_list[2]])
    pop_label4.config(text=artist_name[local_random_list[3]])

    random_number = random.randrange(1,5)
    print(random_number)

    player = vlc.MediaPlayer(preview_url[local_random_list[random_number-1]])
    player.audio_set_volume(25)
    print("Playing!",)
    player.play()

    time_spent = 0
    total_time = 5
    while(time_spent<total_time):
        time.sleep(0.05)
        pop_bar['value'] += 0.99
        window.update_idletasks()
        pop_frame.update()
        #print(time_spent)
        time_spent += 0.05
    pop_bar['value'] = 0

    player.stop()
    print("PLAYED SONG NUMBER:",random_number)
    global song_number
    song_number = random_number
    print(song_number)

def rock_start():
    print("LOCAL RANDOM LIST:", local_random_list)
    for k in range(len(local_random_list)):
        print(preview_url[local_random_list[k]])
    
    rock_label1.config(text=artist_name[local_random_list[0]])
    rock_label2.config(text=artist_name[local_random_list[1]])
    rock_label3.config(text=artist_name[local_random_list[2]])
    rock_label4.config(text=artist_name[local_random_list[3]])

    random_number = random.randrange(1,5)
    print(random_number)

    player = vlc.MediaPlayer(preview_url[local_random_list[random_number-1]])
    player.audio_set_volume(25)
    print("Playing!",)
    player.play()

    time_spent = 0
    total_time = 5
    while(time_spent<total_time):
        time.sleep(0.05)
        rock_bar['value'] += 0.99
        window.update_idletasks()
        rock_frame.update()
        #print(time_spent)
        time_spent += 0.05
    rock_bar['value'] = 0

    player.stop()
    print("PLAYED SONG NUMBER:",random_number)
    global song_number
    song_number = random_number
    print(song_number)

def custom_game_start():
    print("LOCAL RANDOM LIST:", local_random_list)
    for k in range(len(local_random_list)):
        print(preview_url[local_random_list[k]])
    
    custom_game_label1.config(text=artist_name[local_random_list[0]])
    custom_game_label2.config(text=artist_name[local_random_list[1]])
    custom_game_label3.config(text=artist_name[local_random_list[2]])
    custom_game_label4.config(text=artist_name[local_random_list[3]])

    random_number = random.randrange(1,5)
    print(random_number)

    player = vlc.MediaPlayer(preview_url[local_random_list[random_number-1]])
    player.audio_set_volume(25)
    print("Playing!",)
    player.play()

    time_spent = 0
    total_time = 5
    while(time_spent<total_time):
        time.sleep(0.05)
        custom_game_bar['value'] += 0.99
        window.update_idletasks()
        custom_game_frame.update()
        #print(time_spent)
        time_spent += 0.05
    custom_game_bar['value'] = 0

    player.stop()
    print("PLAYED SONG NUMBER:",random_number)
    global song_number
    song_number = random_number
    print(song_number)


# BUTTONS ACTIONS
def btn_clicked():
    print("Button Clicked")

def rap_btn_clicked():
    print("Rap Button Clicked")
    global username_scoreboard
    username_scoreboard = entry0.get()
    print(username_scoreboard)
    rap_frame.tkraise()
    get_data(rap_playlist)
    for i in range(len(preview_url)):
        print(artist_name[i])
        print(preview_url[i])
        print()
    randomize_list()
    randomize_local_list()
    rap_start()

def pop_btn_clicked():
    print("Pop Button Clicked")
    global username_scoreboard
    username_scoreboard = entry0.get()
    print(username_scoreboard)
    pop_frame.tkraise()
    get_data(pop_playlist)
    for i in range(len(preview_url)):
        print(artist_name[i])
        print(preview_url[i])
        print()
    randomize_list()
    randomize_local_list()
    pop_start()

def rock_btn_clicked():
    print("Rock Button Clicked")
    global username_scoreboard
    username_scoreboard = entry0.get()
    print(username_scoreboard)
    rock_frame.tkraise()
    get_data(rock_playlist)
    for i in range(len(preview_url)):
        print(artist_name[i])
        print(preview_url[i])
        print()
    randomize_list()
    randomize_local_list()
    rock_start()
    

def pre_custom_game_btn_clicked():
    print("Pre Custom Game Button Clicked")
    pre_custom_game_frame.tkraise()

def custom_game_btn_clicked():
    print("Custom Game Button Clicked")

    global custom_game_playlist
    custom_game_playlist = pre_custom_game_entry0.get()
    print(custom_game_playlist)

    global username_scoreboard
    username_scoreboard = entry0.get()
    print(username_scoreboard)
    custom_game_frame.tkraise()
    get_data(custom_game_playlist)
    for i in range(len(preview_url)):
        print(artist_name[i])
        print(preview_url[i])
        print()
    randomize_list()
    randomize_local_list()
    custom_game_start()

def scoreboard_btn_clicked():
    print("Scoreboard Button Clicked")
    initialize_database()
    scoreboard_frame.tkraise()
    

#GUI INITIALIZER
window = Tk()
main_frame = Frame()
rap_frame = Frame()
pop_frame = Frame()
rock_frame = Frame()
custom_game_frame = Frame()
scoreboard_frame = Frame()
pre_custom_game_frame = Frame()

for frame in (main_frame,pre_custom_game_frame, rap_frame, pop_frame, rock_frame, custom_game_frame, scoreboard_frame,):
    frame.grid(row=0,column=0,sticky='nsew')

window.geometry("1000x600")
window.configure(bg = "#ffffff")


#=======================+++++>MAIN WINDOW
canvas = Canvas(
    main_frame,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
#canvas.place(x = 0, y = 0)
canvas.pack(expand=YES, fill=BOTH)

background_img = PhotoImage(file = f"MainWindow/background.png")
background = canvas.create_image(
    484.5, 299.5,
    image=background_img)

entry0_img = PhotoImage(file = f"MainWindow/img_textBox0.png")
entry0_bg = canvas.create_image(
    772.5, 201.5,
    image = entry0_img)

#USERNAME ENTRY
entry0 = Entry(
    main_frame,
    bd = 0,
    bg = "#c4c4c4",
    highlightthickness = 0)

entry0.place(
    x = 568, y = 184,
    width = 409,
    height = 33)

img0 = PhotoImage(file = f"MainWindow/img0.png")
b0 = Button(
    main_frame,
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = pre_custom_game_btn_clicked,
    relief = "flat")

b0.place(
    x = 568, y = 431,
    width = 409,
    height = 50)

img1 = PhotoImage(file = f"MainWindow/img1.png")
b1 = Button(
    main_frame,
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = rock_btn_clicked,
    relief = "flat")

b1.place(
    x = 857, y = 308,
    width = 120,
    height = 43)

img2 = PhotoImage(file = f"MainWindow/img2.png")
b2 = Button(
    main_frame,
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = pop_btn_clicked,
    relief = "flat")

b2.place(
    x = 714, y = 308,
    width = 120,
    height = 43)

img3 = PhotoImage(file = f"MainWindow/img3.png")
b3 = Button(
    main_frame,
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = rap_btn_clicked,
    relief = "flat")

b3.place(
    x = 568, y = 308,
    width = 120,
    height = 43)

img4 = PhotoImage(file = f"MainWindow/img4.png")
b4 = Button(
    main_frame,
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = scoreboard_btn_clicked,
    relief = "flat")

b4.place(
    x = 832, y = 538,
    width = 147,
    height = 41)
main_frame.tkraise()


#============================>RAP WINDOW
rap_canvas = Canvas(
    rap_frame,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
rap_canvas.place(x = 0, y = 0)

rap_background_img = PhotoImage(file = f"RapWindow/background.png")
rap_background = rap_canvas.create_image(
    506.0, 298.5,
    image=rap_background_img)

rap_entry0_img = PhotoImage(file = f"RapWindow/img_textBox0.png")
rap_entry0_bg = rap_canvas.create_image(
    220.0, 506.0,
    image = rap_entry0_img)

rap_entry0 = Entry(
    rap_frame,
    bd = 0,
    bg = "#bebebe",
    highlightthickness = 0)

rap_entry0.place(
    x = 174, y = 491,
    width = 92,
    height = 28)

rap_img0 = PhotoImage(file = f"RapWindow/img0.png")
rap_b0 = Button(
    rap_frame,
    image = rap_img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:rap_guess_song(),
    relief = "flat")

rap_b0.place(
    x = 80, y = 543,
    width = 126,
    height = 29)

'''
rap_img1 = PhotoImage(file = f"RapWindow/img1.png")
rap_b1 = Button(
    rap_frame,
    image = rap_img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:rap_start(),
    relief = "flat")

rap_b1.place(
    x = 130, y = 95,
    width = 120,
    height = 30)
'''
# SONG LABELS
rap_label1 = Label(
    rap_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#fff8e8'
)
rap_label1.place(
    x = 80, y = 180
    )

rap_label2 = Label(
    rap_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#c2c5ca'
)
rap_label2.place(
    x = 80, y = 245
    )

rap_label3 = Label(
    rap_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#fff8e8'
)
rap_label3.place(
    x = 80, y = 305
    )

rap_label4 = Label(
    rap_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#c2c5ca'
)
rap_label4.place(
    x = 80, y = 370
    )

#SCORE LABEL
rap_label5 = Label(
    rap_frame,
    text = "0",
    font = ("Roboto",25),
    bg = 'white'
)
rap_label5.place(
    x = 285, y = 23
    )

#STATUS BAR
style = ttk.Style()
style.theme_use('alt')
style.configure("yellow.Horizontal.TProgressbar",
            foreground='yellow', background='yellow')

rap_bar = ttk.Progressbar(
    rap_frame,
    orient=HORIZONTAL,
    length=450,
    style="yellow.Horizontal.TProgressbar")
#bar.pack(pady=10)
rap_bar.place(
    x = 25, y = 130
)


#============================>POP WINDOW
pop_canvas = Canvas(
    pop_frame,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
pop_canvas.place(x = 0, y = 0)

pop_background_img = PhotoImage(file = f"PopWindow/background.png")
pop_background = pop_canvas.create_image(
    549.5, 300.0,
    image=pop_background_img)

pop_entry0_img = PhotoImage(file = f"PopWindow/img_textBox0.png")
pop_entry0_bg = pop_canvas.create_image(
    220.0, 506.0,
    image = pop_entry0_img)

pop_entry0 = Entry(
    pop_frame,
    bd = 0,
    bg = "#bebebe",
    highlightthickness = 0)

pop_entry0.place(
    x = 174, y = 491,
    width = 92,
    height = 28)

pop_img0 = PhotoImage(file = f"PopWindow/img0.png")
pop_b0 = Button(
    pop_frame,
    image = pop_img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:pop_guess_song(),
    relief = "flat")

pop_b0.place(
    x = 80, y = 543,
    width = 126,
    height = 29)

'''
pop_img1 = PhotoImage(file = f"PopWindow/img1.png")
pop_b1 = Button(
    pop_frame,
    image = pop_img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:pop_start(),
    relief = "flat")

pop_b1.place(
    x = 130, y = 95,
    width = 120,
    height = 30)
'''
# SONG LABELS
pop_label1 = Label(
    pop_frame,
    text = "SongTest1",
    font = ("Roboto",16),
    bg = '#fff8e8'
)
pop_label1.place(
    x = 80, y = 180
    )

pop_label2 = Label(
    pop_frame,
    text = "SongTest2",
    font = ("Roboto",16),
    bg = '#c4f6c7'
)
pop_label2.place(
    x = 80, y = 245
    )

pop_label3 = Label(
    pop_frame,
    text = "SongTest3",
    font = ("Roboto",16),
    bg = '#fff8e8'
)
pop_label3.place(
    x = 80, y = 305
    )

pop_label4 = Label(
    pop_frame,
    text = "SongTest4",
    font = ("Roboto",16),
    bg = '#c4f6c7'
)
pop_label4.place(
    x = 80, y = 370
    )

#SCORE LABEL
pop_label5 = Label(
    pop_frame,
    text = "0",
    font = ("Roboto",25),
    bg = 'white'
)
pop_label5.place(
    x = 285, y = 23
    )

#STATUS BAR
style = ttk.Style()
style.theme_use('alt')
style.configure("green.Horizontal.TProgressbar",
            foreground='green', background='green')

pop_bar = ttk.Progressbar(
    pop_frame,
    orient=HORIZONTAL,
    length=450,
    style="green.Horizontal.TProgressbar")
#bar.pack(pady=10)
pop_bar.place(
    x = 25, y = 130
)


#============================>ROCK WINDOW
rock_canvas = Canvas(
    rock_frame,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
rock_canvas.place(x = 0, y = 0)

rock_background_img = PhotoImage(file = f"RockWindow/background.png")
rock_background = rock_canvas.create_image(
    595.5, 298.5,
    image=rock_background_img)

rock_entry0_img = PhotoImage(file = f"RockWindow/img_textBox0.png")
rock_entry0_bg = rock_canvas.create_image(
    220.0, 506.0,
    image = rock_entry0_img)

rock_entry0 = Entry(
    rock_frame,
    bd = 0,
    bg = "#bebebe",
    highlightthickness = 0)

rock_entry0.place(
    x = 174, y = 491,
    width = 92,
    height = 28)

rock_img0 = PhotoImage(file = f"RockWindow/img0.png")
rock_b0 = Button(
    rock_frame,
    image = rock_img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:rock_guess_song(),
    relief = "flat")

rock_b0.place(
    x = 80, y = 543,
    width = 126,
    height = 29)

# SONG LABELS
rock_label1 = Label(
    rock_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#fff8e8'
)
rock_label1.place(
    x = 80, y = 180
    )

rock_label2 = Label(
    rock_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#fee7e4'
)
rock_label2.place(
    x = 80, y = 245
    )

rock_label3 = Label(
    rock_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#fff8e8'
)
rock_label3.place(
    x = 80, y = 305
    )

rock_label4 = Label(
    rock_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#fee7e4'
)
rock_label4.place(
    x = 80, y = 370
    )

#SCORE LABEL
rock_label5 = Label(
    rock_frame,
    text = "0",
    font = ("Roboto",25),
    bg = 'white'
)
rock_label5.place(
    x = 285, y = 23
    )

#STATUS BAR
style = ttk.Style()
style.theme_use('alt')
style.configure("red.Horizontal.TProgressbar",
            foreground='red', background='red')

rock_bar = ttk.Progressbar(
    rock_frame,
    orient=HORIZONTAL,
    length=450,
    style="red.Horizontal.TProgressbar")
#bar.pack(pady=10)
rock_bar.place(
    x = 25, y = 130
)


#============================>PRE CUSTOM GAME WINDOW
pre_custom_game_canvas = Canvas(
    pre_custom_game_frame,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
pre_custom_game_canvas.place(x = 0, y = 0)

pre_custom_game_background_img = PhotoImage(file = f"PreCustom_GameWindow/background.png")
pre_custom_game_background = pre_custom_game_canvas.create_image(
    500.0, 403.5,
    image=pre_custom_game_background_img)

pre_custom_game_entry0_img = PhotoImage(file = f"PreCustom_GameWindow/img_textBox0.png")
pre_custom_game_entry0_bg = pre_custom_game_canvas.create_image(
    499.0, 148.0,
    image = pre_custom_game_entry0_img)

pre_custom_game_entry0 = Entry(
    pre_custom_game_frame,
    bd = 0,
    bg = "#b2b2b2",
    highlightthickness = 0)

pre_custom_game_entry0.place(
    x = 142, y = 133,
    width = 714,
    height = 28)

pre_custom_game_img0 = PhotoImage(file = f"PreCustom_GameWindow/img0.png")
pre_custom_game_b0 = Button(
    pre_custom_game_frame,
    image = pre_custom_game_img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:custom_game_btn_clicked(),
    relief = "flat")

pre_custom_game_b0.place(
    x = 428, y = 194,
    width = 141,
    height = 37)


#============================>CUSTOM GAME WINDOW
custom_game_canvas = Canvas(
    custom_game_frame,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
custom_game_canvas.place(x = 0, y = 0)

custom_game_background_img = PhotoImage(file = f"Custom_GameWindow/background.png")
custom_game_background = custom_game_canvas.create_image(
    453.0, 298.5,
    image=custom_game_background_img)

custom_game_entry0_img = PhotoImage(file = f"Custom_GameWindow/img_textBox0.png")
custom_game_entry0_bg = custom_game_canvas.create_image(
    220.0, 506.0,
    image = custom_game_entry0_img)

custom_game_entry0 = Entry(
    custom_game_frame,
    bd = 0,
    bg = "#bebebe",
    highlightthickness = 0)

custom_game_entry0.place(
    x = 174, y = 491,
    width = 92,
    height = 28)

custom_game_img0 = PhotoImage(file = f"Custom_GameWindow/img0.png")
custom_game_b0 = Button(
    custom_game_frame,
    image = custom_game_img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:custom_game_guess_song(),
    relief = "flat")

custom_game_b0.place(
    x = 80, y = 543,
    width = 126,
    height = 29)

# SONG LABELS
custom_game_label1 = Label(
    custom_game_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#fac2ce'
)
custom_game_label1.place(
    x = 80, y = 180
    )

custom_game_label2 = Label(
    custom_game_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#c5c6cc'
)
custom_game_label2.place(
    x = 80, y = 245
    )

custom_game_label3 = Label(
    custom_game_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#fac2ce'
)
custom_game_label3.place(
    x = 80, y = 305
    )

custom_game_label4 = Label(
    custom_game_frame,
    text = "",
    font = ("Roboto",16),
    bg = '#c5c6cc'
)
custom_game_label4.place(
    x = 80, y = 370
    )

#SCORE LABEL
custom_game_label5 = Label(
    custom_game_frame,
    text = "0",
    font = ("Roboto",25),
    bg = 'white'
)
custom_game_label5.place(
    x = 285, y = 23
    )

#STATUS BAR
style = ttk.Style()
style.theme_use('alt')
style.configure("grey.Horizontal.TProgressbar",
            foreground='grey', background='grey')

custom_game_bar = ttk.Progressbar(
    custom_game_frame,
    orient=HORIZONTAL,
    length=450,
    style="grey.Horizontal.TProgressbar")
#bar.pack(pady=10)
custom_game_bar.place(
    x = 25, y = 130
)


#============================>SCOREBOARD WINDOW
scoreboard_canvas = Canvas(
    scoreboard_frame,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
scoreboard_canvas.place(x = 0, y = 0)

scoreboard_background_img = PhotoImage(file = f"ScoreboardWindow/background.png")
scoreboard_background = scoreboard_canvas.create_image(
    500.0, 300.0,
    image=scoreboard_background_img)

#Scoreboard list
style_scoreboard = ttk.Style(scoreboard_frame)
style_scoreboard.theme_use("clam")

cols = ('username','category','score','playlist_url')
scoreboard_treeview = ttk.Treeview(
    scoreboard_frame,
    columns = cols,
    show = 'headings',
)
#===================================================================================

# STARTING GUI
window.iconphoto(False, PhotoImage(file='icon.png'))
window.title("Song Guesser Game!")

window.resizable(False, False)
window.mainloop()