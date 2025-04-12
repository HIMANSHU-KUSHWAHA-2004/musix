import tkinter as tk
import os
import pygame
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk

pygame.mixer.init()

# Initialize global variables
isplaying = False
current_song = None
playback_position = 0
song_positions = {}
dictionary = {}  # Song path dictionary

def seek_forward():
    global playback_position
    if isplaying:
        current_pos = pygame.mixer.music.get_pos() / 1000  # Get position in seconds
        new_pos = min(current_pos + 10, song_positions.get(current_song, 0))
        pygame.mixer.music.set_pos(new_pos)
        playback_position = new_pos

def seek_backward():
    global playback_position
    if isplaying:
        current_pos = pygame.mixer.music.get_pos() / 1000  # Get position in seconds
        new_pos = max(0, current_pos - 10)
        pygame.mixer.music.set_pos(new_pos)
        playback_position = new_pos

def stop_song():
    global playback_position, isplaying
    if isplaying:
        # Get current position in seconds
        pos = pygame.mixer.music.get_pos() / 1000
        if pos >= 0:  # Only save valid positions
            playback_position = pos
            song_positions[current_song] = playback_position
        pygame.mixer.music.stop()
        isplaying = False

def playsong():
    global isplaying, current_song, playback_position
    selected_song_name = listbox.get(tk.ACTIVE).strip()
    path = dictionary[selected_song_name]
    
    if isplaying and current_song == path:
        # If same song is playing, resume from saved position
        pygame.mixer.music.play(start=playback_position)
        return
        
    # Stop current song if different one is selected
    if isplaying:
        stop_song()
    
    pygame.mixer.music.load(path)
    
    # Check if we have a saved position for this song
    if path in song_positions and song_positions[path] > 0:
        playback_position = song_positions[path]
        pygame.mixer.music.play(start=playback_position)
    else:
        pygame.mixer.music.play()
        playback_position = 0
        
    isplaying = True
    current_song = path

def previous_song():
    global current_song, isplaying, playback_position
    if listbox.size() == 0:
        return
    current_index = listbox.curselection()[0] if listbox.curselection() else 0
    previous_index = (current_index - 1) % listbox.size()
    listbox.select_clear(0, tk.END)
    listbox.select_set(previous_index)
    listbox.activate(previous_index)
    if isplaying:
        playback_position = 0
    playsong()

def next_song():
    global current_song, isplaying, playback_position
    if listbox.size() == 0:
        return
    current_index = listbox.curselection()[0] if listbox.curselection() else 0
    next_index = (current_index + 1) % listbox.size()
    listbox.select_clear(0, tk.END)
    listbox.select_set(next_index)
    listbox.activate(next_index)
    if isplaying:
        playback_position = 0
    playsong()

def stop_song():
    global playback_position,isplaying
    if isplaying:
        pygame.mixer.music.stop()
        playback_position = pygame.mixer.music.get_pos()
        print(playback_position)
        isplaying = False
    
def toggle_button():
    global isplaying
    if isplaying:
        stop_song()
        toggle_but.config(image=stop)
        
    else:
        playsong()
        toggle_but.config(image=play)
    
    

def fill(directory):
    if os.path.isdir(directory) == False:
        return FileExistsError
        
    try:
        
        files = os.listdir(directory)
        if files == False:
            return FileNotFoundError
        else:
                global file,dictionary
                listbox.delete(0, tk.END)
                button1.destroy()
                dictionary = {}
                for file in files:
                    padded = " " + file
                    file_path = os.path.join(directory,file)
                    "this will display the path of we leave here so we modify it using only base name"
                    file_basename = os.path.basename(file_path)
                    dictionary[file_basename] = file_path
                    listbox.insert(tk.END,file_basename)
                    "NOW WE HAVE MAPPED ALL THE SONG WITH THERE PATH NOW WE USE THIS IN THE playsonG"
                    
    except PermissionError:
        return PermissionError
    
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        fill(directory)

# Create the main window
window = tk.Tk()

# Set window size
window.geometry("1000x600")
window.config(background="blue")

# Create a Frame to hold the Canvas and Scrollbar
song_frame = tk.Frame(window, bg="yellow")
song_frame.place(x=550, y=80,height=520,width=450)

heading = tk.Label(window,text="SONGS LIST",font=("Georgia",36, "italic"),bg="#19282F",fg="WHITE",borderwidth=5,relief="raised")
heading.place(x=550,y=0,width=450)

# Create a Canvas widget inside the Frame
listbox = tk.Listbox(song_frame, bg="black", foreground="white", selectmode=tk.SINGLE,
                    relief="sunken", bd=2, font=("Georgia", 20, "italic"))
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

"""THESE SETTING CONNECT THE LISTBOX TO THE FRAME LIKE THAT IF WE NOW INCREASE THE FRAME SIZE THEN THE SIZE OF THE LIST ALSO INCREASE 
AND IF WE DECREASE THE FRAME SIZE THEN THE SIZE OF THE LIST ALSO DECREASE"""

# Create a Scrollbar and attach it to the Canvas
scrollbar = tk.Scrollbar(song_frame, orient=tk.VERTICAL,command=listbox.yview)
"the command is an important step to attach the scrollbar to the canvas it has many funcitonlike the speed and where to move"
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
""" THIS WILL CONFIG MEANS WHEN WE USE THE SCROLLBAR IT WILL GO UP THIS IS COMMEN FOR ALL LIKE IF I USE canvas OR frame WHEN WE NEED TO USE THE THEM LIKE
    WE NEED TO CONFIG THEM HERE WE USE THE """

# SONF FILLING BY THE SELECTED FOLDER
button1 = tk.Button(song_frame,text="Select Directory", command=select_directory,font=("Georgia",20, "italic"),foreground="white",activebackground = "green",background="green",activeforeground="white",borderwidth=5,relief="raised",cursor="hand2")
button1.place(x=125,y=150,width=220)

"when we use the END this will end the item in the last of the list"

path = "pics/peak.jpg"
photo = ImageTk.PhotoImage(Image.open(path))
img_frame = tk.Label(window,image=photo)
img_frame.place(x=0,y=0,height=600,width=550)


icon_frame = tk.Frame(window,bg="white")
icon_frame.place(x=0,y=510,height=100,width=550)


# Seek backward button (10 seconds)
seek_back_img = "pics/back.png"
pic_seek_back = ImageTk.PhotoImage(Image.open(seek_back_img))
seek_back_btn = tk.Button(icon_frame, image=pic_seek_back, relief='raised',
                         borderwidth=5, command=previous_song)
seek_back_btn.place(x=0, y=0, width=110, height=90)

# Previous song button
prev_img = "pics/previous.png"
pic_prev = ImageTk.PhotoImage(Image.open(prev_img))
prev_btn = tk.Button(icon_frame, image=pic_prev, relief='raised',
                    borderwidth=5, command = seek_backward)
prev_btn.place(x=110, y=0, width=110, height=90)


# ----------------------------------------------------------------------------STOP AND PLAY LOGO----------------------------------------------------------------------
play_but = "pics/pause.png"
play = ImageTk.PhotoImage(Image.open(play_but))
stop_but = "pics/play-button.png"
stop = ImageTk.PhotoImage(Image.open(stop_but))


toggle_but = tk.Button(icon_frame,image=stop,height=75,relief='raised',borderwidth=5,command=toggle_button)
toggle_but.place(x=220, y=0,width=110)

# Seek forward button (10 seconds)
seek_forward_img = "pics/next-button.png"
pic_seek_forward = ImageTk.PhotoImage(Image.open(seek_forward_img))
seek_forward_btn = tk.Button(icon_frame, image=pic_seek_forward, relief='raised',
                            borderwidth=5, command=seek_forward)
seek_forward_btn.place(x=330, y=0, width=110, height=90)

# Next song button
next_img = "pics/next.png"
pic_next = ImageTk.PhotoImage(Image.open(next_img))
next_btn = tk.Button(icon_frame, image=pic_next, relief='raised',
                    borderwidth=5, command=next_song)
next_btn.place(x=440, y=0, width=110, height=90)



window.mainloop()