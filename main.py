import customtkinter, tkinter
from tkinter.filedialog import askdirectory
from pytube import YouTube,Playlist
from PIL import Image
import requests
from urllib.request import urlopen
import arabic_reshaper
import re

# App meta data
COLORTHEME = "dark-blue"
RESOLUTION = "640x580"

# App customization
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme(COLORTHEME)

# Sets up the window
app = customtkinter.CTk()
app.geometry(RESOLUTION)
app.title("DownTube")
app.resizable(False,False)

title_label =  customtkinter.CTkLabel(app, text = "\nWelcome to DownTube\n made with love by Nyx/Shnloko <3")
title_label.pack(anchor=tkinter.CENTER)

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx= 60, fill="both", expand=True)
frame.pack_propagate(False)

# Gets input for video or playlist
url_label = customtkinter.CTkLabel(frame, text="Youtube URL:")
url_label.grid(row=0,column=0, pady = (10,0),padx=20)

url_entry = customtkinter.CTkEntry(frame,placeholder_text="www.youtube.com/yourvideo",width=300,fg_color="gray21")
url_entry.grid(row=0,column=1,columnspan=2,pady = (10,0),padx=10)

# Content display logic

def display_content(content):
    title = "ERROR: unrecognized characters"

    eng = re.compile(r"[a-zA-Z0-9]")
    arb = re.compile(r'[ا-ي]')
    
    #TODO: fix Asian chars crashing
    #TODO: add emoji support
    
    if eng.match(content.title):
        title = content.title
        title = title[0:51] + "..." if len(title) > 50 else title
    elif arb.match(content.title):
        reshaped_text = arabic_reshaper.reshape(content.title)
        title = reshaped_text[::-1]
        title = "..."  + title[0:51] if len(title) > 50 else title
    
        
    name_preview_label.configure(text=title)

    # Grabs the thumbnail of the first video incase of playlist
    video = content.videos[0] if isinstance(content,Playlist) else content 
    thumbnail = Image.open(requests.get(video.thumbnail_url, stream = True).raw)

    my_image = customtkinter.CTkImage(light_image=thumbnail, dark_image=thumbnail, size=(60, 40))
    thumbnail_preview_label.configure(image=my_image)


# Check button logic

def unshorten_url(url):

    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url

def check_button():
    url = url_entry.get()

    # Checks if it's shortened
    if url.count("youtu.be/") == 1:
        url = unshorten_url(url)

    # Checks for the type of link
    if url.count("youtube.com/playlist?list=") == 1 or url.count("&list=") == 1:
        # Updates the label and graps playlist
        url_check_label.configure(text="Playlist detected!")
        content = Playlist(url)
        display_content(content)
        construct_download(True,str(len(content)))

    elif url.count("youtube.com/watch?v=") == 1:
        # Updates the label and graps video
        url_check_label.configure(text="Video detected!")
        content = YouTube(url)
        display_content(content)
        construct_download(False,"1")

    else:
        url_check_label.configure(text="Cannot recognize url type :(")
        content = None
        name_preview_label.configure(text="")
        thumbnail_preview_label.configure(image=None)
        construct_download(False,"0")
        
    select_destination_entry.delete(0,'end')


# UI for the check button

url_button_check = customtkinter.CTkButton(frame, text="Check url", command=check_button)
url_button_check.grid(row=1,column=0,pady=10, padx=20)
url_check_label = customtkinter.CTkLabel(frame,anchor="w")
url_check_label.configure(text="")
url_check_label.grid(row=1,column=1)

# Displays content info
name_label = customtkinter.CTkLabel(frame,text="Name: ").grid(row=2, column=0)
name_preview_label = customtkinter.CTkLabel(frame,font=("time",20,"bold"))
name_preview_label.configure(text="")
name_preview_label.grid(row = 2, column=1)

thumbnail_label = customtkinter.CTkLabel(frame,text="Thumbnail: ").grid(row=3, column=0)
thumbnail_preview_label = customtkinter.CTkLabel(frame,text="",image=None)
thumbnail_preview_label.grid(row=3, column=1)

# Download area

downloadframe = customtkinter.CTkFrame(master=frame,width=440)
downloadframe.grid(row=4, columnspan= 2,pady=20, padx= 40)
downloadframe.grid_propagate(False)

# From to section
from_range_label = customtkinter.CTkLabel(master=downloadframe,text="From: ")
from_range_entry = customtkinter.CTkEntry(master=downloadframe,width=125)

from_range_label.grid(row=0,column=0,pady=10, padx=20)
from_range_entry.grid(row=0,column=1,pady=10)
from_range_entry.delete(0,'end')
from_range_entry.configure(fg_color="gray")
from_range_entry.configure(state=tkinter.DISABLED)

to_range_label = customtkinter.CTkLabel(master=downloadframe,text="To: ")
to_range_entry = customtkinter.CTkEntry(master=downloadframe,width=125)

to_range_label.grid(row=0,column=2,pady=10, padx=20)
to_range_entry.grid(row=0,column=3,padx=(0,10),pady=10)
to_range_entry.delete(0,'end')
to_range_entry.configure(fg_color="gray")
to_range_entry.configure(state=tkinter.DISABLED)


# Selecting the destination
def select_folder():
    path = askdirectory(title="Select your folder")
    select_destination_entry.delete(0,'end')
    select_destination_entry.insert(0, path)

select_destination_label = customtkinter.CTkLabel(master=downloadframe,text="destination")
select_destination_entry = customtkinter.CTkEntry(master=downloadframe,width=125,fg_color="gray21")
select_destination_button = customtkinter.CTkButton(master=downloadframe,text="select",width=125,command=select_folder)

select_destination_label.grid(row=1,column=0,padx=20,pady=10)
select_destination_entry.grid(row=1,column=1,pady=10)
select_destination_button.grid(row=1,column=3,pady=10,padx=(0,10))

# Download button and logic
video_button = customtkinter.CTkButton(master=downloadframe,text="Download video",width=160)
video_button.grid(row=2,column=0,columnspan=2,pady=40,padx=20)

audio_button = customtkinter.CTkButton(master=downloadframe,text="Download Audio",width=160)
audio_button.grid(row=2,column=2,columnspan=2,pady=40,padx=20)

def construct_download(is_playlist,length):

    if(is_playlist):
        from_range_entry.configure(state=tkinter.NORMAL)
        from_range_entry.configure(fg_color="gray21")
        to_range_entry.configure(state=tkinter.NORMAL)
        to_range_entry.configure(fg_color="gray21")

        from_range_entry.delete(0,'end')
        from_range_entry.insert(0, "1")
        to_range_entry.delete(0,'end')
        to_range_entry.insert(0, length)
    else:
        from_range_entry.delete(0,'end')
        from_range_entry.configure(fg_color="gray")
        from_range_entry.configure(state=tkinter.DISABLED)

        to_range_entry.delete(0,'end')
        to_range_entry.configure(fg_color="gray")
        to_range_entry.configure(state=tkinter.DISABLED)
        return;

#TODO: Implement logic beind video and audio downloads, add a progressbar and a cancel button and a quality selector

def download_asvideo(content):
    pass

def download_asaudio(content):
    pass


# Display mode list
def change_appearance_mode_event(new_appearance_mode):
   customtkinter.set_appearance_mode(new_appearance_mode)

appearance_mode_optionemenu = customtkinter.CTkOptionMenu(frame, values=["Dark", "Light", "System"], command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=5,padx=20)


app.mainloop()
