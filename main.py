import customtkinter, tkinter
from pytube import YouTube,Playlist
from PIL import Image, ImageTk
import requests
from urllib.request import urlopen

# App meta data
COLORTHEME = "dark-blue"
RESOLUTION = "640x480"
FONT = ("Comic Sans MS",400, "bold")
# App customization
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme(COLORTHEME)

# Setting up the window
app = customtkinter.CTk()
app.geometry(RESOLUTION)
app.title("DownTube")
app.resizable(False,False)

title_label =  customtkinter.CTkLabel(app, text = "\nWelcome to DownTube\n made with love by Nyx/Shnloko <3")
title_label.pack(anchor=tkinter.CENTER)

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx= 60, fill="both", expand=True)


# Get input for video or playlist
input_label = customtkinter.CTkLabel(frame, text="Youtube URL:")
input_label.grid(row=0,column=0, pady = (10,0),padx=20)

url_entry = customtkinter.CTkEntry(frame,placeholder_text="www.youtube.com/yourvideo",width=300)
url_entry.grid(row=0,column=1,columnspan=2,pady = (10,0))

# content info
name_label = customtkinter.CTkLabel(frame,text="Name: ").grid(row=2, column=0)
name_info_label = customtkinter.CTkLabel(frame)
name_info_label.configure(text="")
name_info_label.grid(row = 2, column=1)

thumbnail_label = customtkinter.CTkLabel(frame,text="Thumbnail: ").grid(row=3, column=0)
thumbnail_preview_label = customtkinter.CTkLabel(frame,image=None)

# Checking if its valid and playlist
global content # Where the video or playlist is stored

def unshorten_url(url):

    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url


def url_validation():
    url = url_entry.get()

    # Checks if it's shortened
    if"youtu.be" in url:
        url = unshorten_url(url)

    if "/playlist?list=" in url:

        url_check_label.configure(text="Playlist detected!")
        content = Playlist(url)

        name_info_label.configure(text=content.title)
        #TODO: UPDATE THUMBNAIL

    elif "watch?v=" in url:

        url_check_label.configure(text="Video detected!")
        content = YouTube(url)

        name_info_label.configure(text=content.title)
        #TODO: UPDATE THUMBNAIL

    else:
        url_check_label.configure(text="Cannot recognize url type :(")

url_button_check = customtkinter.CTkButton(frame, text="Check url", command=url_validation)
url_button_check.grid(row=1,column=0,pady=10, padx=20)

url_check_label = customtkinter.CTkLabel(frame,anchor="w")
url_check_label.configure(text="")
url_check_label.grid(row=1,column=1)


# Apperance list
#def change_appearance_mode_event(new_appearance_mode):
#    customtkinter.set_appearance_mode(new_appearance_mode)

#appearance_mode_label = customtkinter.CTkLabel(frame, text="Appearance Mode:", anchor="s")
#appearance_mode_label.grid(padx=20, pady=(10, 0), anchor="w")
#appearance_mode_optionemenu = customtkinter.CTkOptionMenu(frame, values=["Light", "Dark", "System"], command=change_appearance_mode_event)
#appearance_mode_optionemenu.grid(padx=20, pady=(10, 10), anchor="w")


app.mainloop()
