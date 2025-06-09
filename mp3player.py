
import pygame
from pygame import mixer
from tkinter import *
import tkinter.font as font
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import PhotoImage
from mutagen.mp3 import MP3
from tkinter import ttk
import matplotlib.font_manager as fm
import matplotlib as mpl
import random

pygame.init()
SONG_END_EVENT = pygame.USEREVENT
mixer.music.set_endevent(SONG_END_EVENT)
current_song = None
is_seeking = False
default_folder = "C:/Users/grish/csfolders/mp3player/musicmaxxing"
shuffleval = False

def load_folder_songs(folder_path):
    mixer.init()
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            songs_list.insert(END, filename)

#to add new songs, you can either directly add them here or add to the folder!
def addlesongs():
    thesong = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song!", filetypes=(("MP3 Files", ".mp3"),))
    for s in thesong:
        s = os.path.basename(s)  # Get the filename without the path
        songs_list.insert(END, s)

def deletelesong():
    currentsong = songs_list.curselection()
    if currentsong:
        songs_list.delete(currentsong[0])

def update_seeker(): 
    if mixer.music.get_busy():
        if not is_seeking:
            elasped_time = mixer.music.get_pos() / 1000  # Get the elapsed time! 
            seeker.set(elasped_time)  # Music is constantly playing
    checkfortime()
    root.after(1000, update_seeker)  # So update every second!

def update_timer():
    if mixer.music.get_busy():
        elapsed_time = mixer.music.get_pos() / 1000
        timer_label.config(text=f"{timer(elapsed_time)}")
    else:
        timer_label.config(text="00:00")
    root.after(1000, update_timer)

def setdamusic(value):
    global is_seeking
    is_seeking=True
    mixer.music.set_pos(float(value))

def seekerrelease(event=None):
    global is_seeking
    is_seeking=False
    setdamusic(seeker.get())

def timer(seconds):
    minutes=int(seconds // 60)
    seconds=int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"


def Play():
    global current_song
    song = songs_list.get(ACTIVE)
    if mixer.music.get_busy():
        return
    else:
        current_song = song
    song_path = os.path.join("C:/Users/grish/csfolders/mp3player/musicmaxxing/", song)
    try:
        mixer.music.load(song_path)
        mixer.music.play(loops=0)
        print(f"This is gas: {song_path}")
    except Exception as e:
        print(f"song not found: {e}")
    audio = MP3(song_path)
    song_duration = audio.info.length
    elasped_time = mixer.music.get_pos() / 1000
    seeker.config(to=song_duration)  # This sets the max value of the seeker to the length of the song
    getcurrent()
    update_seeker()  #begin updating!
    update_timer() #more updating!
    checkfortime()

def getcurrent():
    global current_song
    current_song = songs_list.get(ACTIVE)
    return current_song

def checkfortime():
    for event in pygame.event.get():
        if event.type == SONG_END_EVENT:
            if shuffletruth == True:
                Shuffle()
            else:
                Next()

def Pause():
    mixer.music.pause()

def Stop():
    mixer.music.stop()
    songs_list.selection_clear(ACTIVE)

def Resume():
    mixer.music.unpause()
    update_seeker()

def Previous():
    previousone = songs_list.curselection()
    if previousone:
        previousone = previousone[0] - 1
        thesong2 = songs_list.get(previousone)
        song_path = os.path.join("C:/Users/grish/csfolders/mp3player/musicmaxxing",thesong2)
        mixer.music.load(song_path)
        mixer.music.play()
        songs_list.selection_clear(0, END)
        songs_list.activate(previousone)
        songs_list.selection_set(previousone)

def Next():
    nextone = songs_list.curselection()
    if nextone:
        nextone = nextone[0] + 1
        thesong3 = songs_list.get(nextone)
        song_path = os.path.join("C:/Users/grish/csfolders/mp3player/musicmaxxing/", thesong3)
        mixer.music.load(song_path)
        mixer.music.play()
        songs_list.selection_clear(0, END)
        songs_list.activate(nextone)
        songs_list.selection_set(nextone)

def Shuffle():
    getcurrent()
    current_song = getcurrent()
    thesongplaying2 = 0
    shuffleone = songs_list.curselection()
    playlistlength = 0
    for item in os.listdir(default_folder):
        item_path = os.path.join("C:/Users/grish/csfolders/mp3player/musicmaxxing/",item)
    if os.path.isfile(item_path):
        playlistlength += 1
    if shuffleone:
        shuffleone = [random.randint(0,playlistlength + 1)] 
        thesong4 = songs_list.get(shuffleone)
        song_path = os.path.join("C:/Users/grish/csfolders/mp3player/musicmaxxing/", thesong4)
        print(current_song)
    if current_song == thesong4:
        Shuffle()
    else:
        thesongplaying2 = getcurrent()
        print("Now playing,",thesong4)
        mixer.music.load(song_path)
        mixer.music.play()
        songs_list.selection_clear(0,END)
        songs_list.activate(shuffleone)
        songs_list.selection_set(shuffleone)
        global shuffletruth;
        shuffleval = True
        shuffletruth = shuffleval
    
def Mute():
    mixer.music.set_volume(0)

def Unmute():
    mixer.music.set_volume(1)
root = Tk()
mixer.init()
play_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/go!button.png")
pause_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/stop!button.png")
stop_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/eject!.png")
resume_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/ya!button.png")
previous_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/goback!button.png")
next_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/goforward!button.png")
add_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/lenewsong!.png")
delete_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/getridofdasong!.png")
icon_img = PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/yo!.png")
shuffle_img=PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/shuffle!.png")
mute_img=PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/mute!.png")
unmute_img=PhotoImage(file="C:/Users/grish/csfolders/mp3player/Assets/unmute!.png")
fe = fm.FontEntry(fname='C:/Users/grish/csfolders/mp3player/Assets/Newsreader-VariableFont_opsz,wght.ttf', name='Newsreader')
fm.fontManager.ttflist.insert(0, fe)
mpl.rcParams['font.family'] = fe.name
root.title("Grish's Pretty Awesome Music Player")
root.geometry("385x400")
root.configure(bg="#120F1B")
root.iconphoto(True, icon_img)
thefont = font.Font(family='Newsreader', size=11)#arial used as fallback, you have to install Newsreader to your system to use it
#I included the steps to start setting up the font in the mp3 player, but you'd have to use a tool to convert it into a format that tkinter understands
#file included with repo
songs_list = Listbox(root, selectmode=SINGLE, bg="#A996EB", fg="#000000", width=41, height=15,font=thefont)
songs_list.grid(row=0, column=0, columnspan=9, padx=10, pady=10)
playbutton = Button(root, image=play_img, bg="#A996EB", font=thefont, command=Play)
playbutton.place(x=10, y=350)
pausebutton = Button(root, image=pause_img, bg="#A996EB", font=thefont, command=Pause)
pausebutton.place(x=50, y=350)
stopbutton = Button(root, image=stop_img, bg="#A996EB", font=thefont, command=Stop)
stopbutton.place(x=130, y=350)
resumebutton = Button(root, image=resume_img, bg="#A996EB", font=thefont, command=Resume)
resumebutton.place(x=90, y=350)
previousbutton = Button(root, image=previous_img, bg="#A996EB", font=thefont, command=Previous)
previousbutton.place(x=170, y=350)
nextbutton = Button(root, image=next_img, bg="#A996EB", font=thefont, command=Next)
nextbutton.place(x=210, y=350)
seeker = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=90, bg="#A996EB", fg="#000000", font=thefont, command=setdamusic)
seeker.place(x=250,y=348)
addbutton = Button(root,image=add_img,bg="#120F1B", font=thefont,command=addlesongs)
addbutton.place(x=346,y=10)
deletebutton=Button(root, image=delete_img,bg="#120F1B",font=thefont,command=deletelesong)
deletebutton.place(x=346,y=50)
timer_label= Label(root, text="00:00", bg="#120F1B", fg="#FFFFFF", font=thefont)
timer_label.place(x=298,y=315)
shufflebutton = Button(root, image=shuffle_img, bg="#120F1B",font=thefont, command=Shuffle)
shufflebutton.place(x=346,y=90)
mutebutton = Button(root, image=mute_img, bg="#120F1B",font=thefont, command=Mute)
mutebutton.place(x=346,y=130)
unmutebutton = mutebutton = Button(root, image=unmute_img, bg="#120F1B",font=thefont, command=Unmute)
unmutebutton.place(x=346,y=170)
themenu = Menu(root)
root.config(menu=themenu)
addsongmenu = Menu(themenu, tearoff=False)
themenu.add_cascade(label="The Menu", menu=addsongmenu)
addsongmenu.add_command(label="Add Songs", command=addlesongs)
addsongmenu.add_command(label="Delete Song", command=deletelesong)

load_folder_songs(default_folder)

mainloop()
