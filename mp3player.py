
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
default_folder = "" #insert your default playlist here 
theplaylist_path = default_folder
shuffletruth = False

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
    global seconds
    if is_seeking==True:
        timer_label.config(text=f"{timer(seconds)}")
    if mixer.music.get_busy():
        elapsed_time = mixer.music.get_pos() / 1000
        timer_label.config(text=f"{timer(elapsed_time)}")
    else:
        timer_label.config(text="00:00")
    root.after(1000, update_timer)

def setdamusic(value):
    global is_seeking
    global seconds
    is_seeking=True
    mixer.music.set_pos(float(value))
    seconds = (float(value))
    timer(seconds)
    update_timer()

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
    global theplaylist_path
    global song_duration
    song = songs_list.get(ACTIVE)
    if mixer.music.get_busy():
        return
    else:
        current_song = song
    song_path = os.path.join(theplaylist_path, song)
    print(song_path)
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
    playingsong = song
    setsongplaying(playingsong)
    progressorreset()
    progressor()

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
        song_path = os.path.join(theplaylist_path,thesong2)
        mixer.music.load(song_path)
        mixer.music.play()
        songs_list.selection_clear(0, END)
        songs_list.activate(previousone)
        songs_list.selection_set(previousone)
        playingsong = thesong2
        setsongplaying(playingsong)
        progressorreset()
        progressor()

def Next():
    nextone = songs_list.curselection()
    if nextone:
        nextone = nextone[0] + 1
        thesong3 = songs_list.get(nextone)
        song_path = os.path.join(theplaylist_path, thesong3)
        mixer.music.load(song_path)
        mixer.music.play()
        songs_list.selection_clear(0, END)
        songs_list.activate(nextone)
        songs_list.selection_set(nextone)
        playingsong = thesong3
        setsongplaying(playingsong)
        progressorreset()
        progressor()

def Shuffle():
    getcurrent()
    current_song = getcurrent()
    thesongplaying2 = 0
    shuffleone = songs_list.curselection()
    playlistlength = 0
    for item in os.listdir(default_folder):
        item_path = os.path.join(theplaylist_path,item)
    if os.path.isfile(item_path):
        playlistlength += 1
    if shuffleone:
        shuffleone = [random.randint(0,playlistlength + 1)] 
        thesong4 = songs_list.get(shuffleone)
        song_path = os.path.join(theplaylist_path, thesong4)
        print(current_song)
    if current_song == thesong4:
        Shuffle()
    else:
        thesongplaying2 = getcurrent()
        playingsong = thesong4
        mixer.music.load(song_path)
        mixer.music.play()
        songs_list.selection_clear(0,END)
        songs_list.activate(shuffleone)
        songs_list.selection_set(shuffleone)
        global shuffletruth;
        shuffleval = True
        shuffletruth = shuffleval
        setsongplaying(playingsong)

def setsongplaying(playingsong):
    max_length = 25 
    truncated_song = playingsong[:max_length] + "..." if len(playingsong) > max_length else playingsong
    print("Now Playing:", truncated_song)
    nowplayinglabel.config(text=f"Now Playing: {truncated_song}")

def Mute():
    mixer.music.set_volume(0)

def Unmute():
    mixer.music.set_volume(1)

def SetVolume(value):
    volume = float(value)/ 100.0
    mixer.music.set_volume(volume)
root = Tk()
mixer.init()

def chooseplaylist():
    global theplaylist_path
    theplaylist_path = filedialog.askdirectory(initialdir="")#path to your playlists folder here, title="Choose a Playlist!")
    if theplaylist_path:
        try:
            fileslist=os.listdir(theplaylist_path)
            playlistfileslist = [f for f in fileslist if f.endswith('.mp3')]
            songs_list.delete(0,END)
            for file_name in playlistfileslist:
                songs_list.insert(END,file_name)
        except Exception as e:
            print("Error!")
def progressor():
    global song_duration
    progressbar.start()
    root.after(song_duration * 1000, progressbar.stop)
def progressorreset():
      progressbar['value']=0
#replace with the path for the assets you downloaded 
previous_img = PhotoImage(file="")
next_img = PhotoImage(file="")
add_img = PhotoImage(file="")
delete_img = PhotoImage(file="")
icon_img = PhotoImage(file="")
shuffle_img=PhotoImage(file="")
back_img=PhotoImage(file="")
fe = fm.FontEntry(fname='', name='Newsreader')#for this to work, you need to download the font to your system.
fm.fontManager.ttflist.insert(0, fe)
mpl.rcParams['font.family'] = fe.name
root.title("Grish's Pretty Awesome Music Player")
root.geometry("400x400")
root.configure(bg="#120F1B")
root.iconphoto(True, icon_img)
thefont = font.Font(family='Arial', size=11)#arial used as fallback, you have to install Newsreader to your system to use it
#I included the steps to start setting up the font in the mp3 player, but you'd have to use a tool to convert it into a format that tkinter understands
#file included with repo
songs_list = Listbox(root, selectmode=SINGLE, bg="#A996EB", fg="#000000", width=41, height=15,font=thefont)
songs_list.grid(row=0, column=0, columnspan=9, padx=10, pady=10)
previousbutton = Button(root, image=previous_img, bg="#A996EB", font=thefont, command=Previous)
previousbutton.place(x=90, y=350)
nextbutton = Button(root, image=next_img, bg="#A996EB", font=thefont, command=Next)
nextbutton.place(x=305, y=350)
seeker = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=166, bg="#A996EB", fg="#000000", font=thefont, command=setdamusic)
seeker.place(x=130,y=348)
addbutton = Button(root,image=add_img,bg="#120F1B", font=thefont,command=addlesongs)
addbutton.place(x=353,y=10)
deletebutton=Button(root, image=delete_img,bg="#120F1B",font=thefont,command=deletelesong)
deletebutton.place(x=353,y=55)
timer_label= Label(root, text="00:00", bg="#120F1B", fg="#FFFFFF", font=thefont)
timer_label.place(x=298,y=315)
shufflebutton = Button(root, image=shuffle_img, bg="#120F1B",font=thefont, command=Shuffle)
shufflebutton.place(x=353,y=100)
volumeslider = Scale(root,from_=100, to=0,length=150, bg="#A996EB", fg="#000000", font=thefont,command = SetVolume)
volumeslider.set(mixer.music.get_volume()*100)
volumeslider.place(x=346,y=188)
progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=150, mode='indeterminate', style='TProgressbar')
progressbar.place(x=10, y=315)
themenu = Menu(root)
root.config(menu=themenu)
addsongmenu = Menu(themenu, tearoff=False)
themenu.add_cascade(label="The Menu", menu=addsongmenu)
addsongmenu.add_command(label="Add Songs", command=addlesongs)
addsongmenu.add_command(label="Delete Song", command=deletelesong)
addsongmenu.add_command(label="Browse Playlists", command=chooseplaylist)
nowplayinglabel = Label(root, text="",bg="#120F1B",fg="#FFFFFF",font=thefont)
nowplayinglabel.place(x=10,y=315)
class MuterButton(tk.Button):
    def __init__(self, parent, images, functions, initial_state=0, **kwargs):
        super().__init__(parent, **kwargs)
        self.images = [PhotoImage(file=image) for image in images]
        self.functions = functions
        self.state = initial_state
        self.config(image=self.images[self.state], command=self.on_click)
        self.image = self.images[self.state] # Keep a reference to the image

    def on_click(self):
        self.state = (self.state + 1) % len(self.images)
        self.config(image=self.images[self.state])
        self.image = self.images[self.state]
        self.functions[self.state]()
if __name__ == "__main__":
    themutebutton = MuterButton(
        root,
        images=["",""], # assets for your mute button
        functions=[Unmute, Mute],
        bg="#120F1B"
    )
    themutebutton.place(x=353,y=145)

class PlayButton(tk.Button):
    def __init__(self, parent, images, functions, initial_state=0, **kwargs): 
        super().__init__(parent, **kwargs)
        self.images = [PhotoImage(file=image) for image in images]
        self.functions = functions
        self.state = initial_state
        self.config(image=self.images[self.state], command=self.on_click)
        self.image = self.images[self.state] # Keep a reference to the image
    def on_click(self):
        self.state = (self.state + 1) % len(self.images)
        self.config(image=self.images[self.state])
        self.image = self.images[self.state]
        self.functions[self.state]()
if __name__ == "__main__":
    theplaybutton = PlayButton(
    root,
    images=["",""],#assets for your play button
    functions=[Resume,Pause],
    bg="#121214"
    )
    theplaybutton.place(x=10,y=350)

class LoadButton(tk.Button):
    def __init__(self, parent, images, functions, initial_state=0, **kwargs): 
        super().__init__(parent, **kwargs)
        self.images = [PhotoImage(file=image) for image in images]
        self.functions = functions
        self.state = initial_state
        self.config(image=self.images[self.state], command=self.on_click)
        self.image = self.images[self.state] # Keep a reference to the image
    def on_click(self):
        self.state = (self.state + 1) % len(self.images)
        self.config(image=self.images[self.state])
        self.image = self.images[self.state]
        self.functions[self.state]()
if __name__ == "__main__":
    theloadbutton = LoadButton(
    root,
    images=["",""],#assets for your 
    functions=[Stop,Play],
    bg="#A996EB"
    )
    theloadbutton.place(x=50,y=350)
load_folder_songs(default_folder)
mainloop()
