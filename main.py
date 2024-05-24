import time
import tkinter
import customtkinter
import yt_dlp
# import pytube
# from pytube import YouTube
# from pytube import Playlist
import os
from youtube_search import YoutubeSearch
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD

class Tk(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

app = Tk()
app.geometry("720x480")
app.title("Youtube downloader")
#v to trzeba zakomentować, by .py do .exe zadziałało
# app.iconbitmap('yt.ico')
basedir = os.path.dirname(__file__)
app.iconbitmap(os.path.join(basedir, "yt.ico"))
option_frame = customtkinter.CTkFrame(app, fg_color = 'transparent')

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass
    
    def error(self, msg):
        print(msg)

def my_hook(d):
    finishLabel.configure(text_color = 'white')
    if d['status'] == 'downloading':
        progress = d['_percent_str']
        try:
            a = round(d['speed']/1048576, 2)
            speed = f'{a}MiB/s'
        except:
            speed = 'Nie wiadomo' 
        finishLabel.configure(text=f'postęp: {progress} | prędkość: {speed}')

        app.update_idletasks()
    if d['status'] == 'finished':
        dots = ''
        for i in range(3):
            dots += '.'
            finishLabel.configure(text='Przetwarzanie' + dots)
            time.sleep(1)

ydl_opts = {
    'format': 'bestaudio/best', 
    'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'outtmpl': '%(title)s',
    'noplaylist': True
}

ydl_opts2 = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
    'outtmpl': '%(title)s',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'noplaylist': True
}

jakosc = ['320', '256', '224', '192', '160', '128']
rozdzielczosc = ['2160', '1440', '1080', '720', '480', '360', '240', '144']
codecs = ['mp3', 'wav', 'flac', 'opus', 'vorbis']
extensions = ['mp4', 'webm', 'mkv']

polish_names = {
    "Documents": "Dokumenty",
    "Desktop": "Pulpit",
    "Downloads": "Pobrane",
    "Videos": "Wideo",
    "Pictures": "Obrazy",
    "Music": "Muzyka",
    "Desktop": "Pulpit"
}

def get_path(event):
    path = event.data

    file_name = os.path.basename(path)
    extension = os.path.splitext(file_name)[1]

    if extension == '':
        # Remove curly brackets from the beginning and end of the path
        path = path.strip('{}')

        # Split the path using space as the delimiter
        path_parts = path.split(' ')
        
        # Check if the last part ends with a curly bracket
        last_part = path_parts[-1]
        if last_part.endswith('}'):
            # Remove the curly bracket from the last part
            last_part = last_part[:-1]
            path_parts[-1] = last_part

        # Join the parts to reconstruct the folder path
        folder_path = ' '.join(path_parts)
        folder_name = os.path.basename(folder_path)

        folder_path_label.configure(text=folder_path)

        if folder_name in polish_names:
            folder_name = polish_names[folder_name]
        else:
            folder_name = os.path.basename(folder_path)

        browse_button.configure(text='Wybrano:\n' + folder_name)


def browse_folder():
    folder_path = customtkinter.filedialog.askdirectory()
    if folder_path:
        folder_name = os.path.basename(folder_path)
        # folder_name_label.configure(text=folder_name)
        folder_path_label.configure(text=folder_path)
        if folder_name in polish_names:
            folder_name = polish_names[folder_name]
        else:
            folder_name = os.path.basename(folder_path)
        browse_button.configure(text='Wybrano:\n' + folder_name)

def JakiTheme(m):
    if m == 'ciemny':
        theme.configure(text_color="gray30", fg_color='gray70', command=lambda m="jasny": JakiTheme(m))
        customtkinter.set_appearance_mode("Light")
        finishLabel.configure(text_color = 'gray12')
    else:
        theme.configure(text_color="gainsboro", fg_color='gray38', command=lambda m="ciemny": JakiTheme(m))    
        customtkinter.set_appearance_mode("Dark")
        finishLabel.configure(text_color = 'white')

def ShowCommands(m):
    if m == 'info':
        info.configure(command=lambda m="nieinfo": ShowCommands(m))
        title.pack_forget()
        link.pack_forget()
        finishLabel.pack_forget()
        wybor.pack_forget()
        jakoscLabel.pack_forget()
        wyborcodeca.pack_forget()
        mp3jakosc.pack_forget()
        option_frame.pack_forget()
        mp4rozdzielczosc.pack_forget()
        download.pack_forget()
        browse_button.pack_forget()
        CheckName.pack_forget()
        CustomName.pack_forget()
        # help.pack()
        help.place(anchor='n', relx = 0.5, rely = 0.05)
    elif m == 'nieinfo' and wybor.get() == 'Muzyka':
        info.configure(command=lambda m="info": ShowCommands(m))
        # help.pack_forget()
        help.place_forget()
        CheckName.pack_forget()
        CustomName.pack_forget()
        title.pack(padx=10, pady=10)
        link.pack()
        finishLabel.pack(pady=5)
        wybor.pack(pady=5)
        jakoscLabel.pack(pady=5)
        wyborcodeca.pack(side='left', pady=5, padx=5)
        mp3jakosc.pack(pady=5, padx=5)
        option_frame.pack()
        browse_button.pack(pady=5)
        download.pack(padx=10, pady=5)
        CheckName.pack(pady=5)
        if CheckName.get() == 1:
            CustomName.pack(pady=5)
    else:
        info.configure(command=lambda m="info": ShowCommands(m))
        # help.pack_forget()
        help.place_forget()
        option_frame.pack_forget()
        CheckName.pack_forget()
        CustomName.pack_forget()
        title.pack(padx=10, pady=10)
        link.pack()
        finishLabel.pack(pady=5)
        wybor.pack(pady=5)
        jakoscLabel.pack(pady=5)
        wyborextension.pack(side='left', pady=5, padx=5)
        mp4rozdzielczosc.pack(pady=5, padx=5)
        option_frame.pack()
        browse_button.pack(pady=5)
        download.pack(padx=10, pady=5)
        CheckName.pack(pady=5)
        if CheckName.get() == 1:
            CustomName.pack(pady=5)
    # else:
    #     info.configure(command=lambda m="info": ShowCommands(m))
    #     help.pack_forget()
    #     title.pack(padx=10, pady=10)
    #     link.pack()
    #     finishLabel.pack(pady=5)
    #     wybor.pack(pady=5)
    #     jakoscLabel.pack(pady=5)
    #     mp4rozdzielczosc.pack(pady=5)
    #     browse_button.pack(pady=5)
    #     download.pack(padx=10, pady=5)     

def WidocznoscElementow(*args):
    if wybor.get() == 'Muzyka':
        jakoscLabel.configure(text='Bitrate (w kbps)')
        wyborextension.pack_forget()
        mp4rozdzielczosc.pack_forget()
        # option_frame2.pack_forget()
        wyborcodeca.pack(side='left', pady=5, padx=5)
        mp3jakosc.pack(pady=5, padx=5)
        option_frame.pack()
        browse_button.pack_forget()
        browse_button.pack(pady=5)
        download.pack_forget()
        download.pack(padx=10, pady=5)
        CheckName.pack_forget()
        CheckName.pack(pady=5)
        CustomName.pack_forget()
        if CheckName.get() == 1:
            CustomName.pack(pady=5)
        # folder_name_label.pack_forget()
        # folder_name_label.pack(pady=5)
        # folder.pack_forget()
        # folder.pack(pady=10)
    else:
        jakoscLabel.configure(text='Jakość')
        wyborcodeca.pack_forget()
        mp3jakosc.pack_forget()
        option_frame.pack_forget()
        wyborextension.pack(side='left', pady=5, padx=5)
        mp4rozdzielczosc.pack(pady=5, padx=5)
        option_frame.pack()
        browse_button.pack_forget()
        browse_button.pack(pady=5)
        download.pack_forget()
        download.pack(padx=10, pady=5)
        CheckName.pack_forget()
        CheckName.pack(pady=5)
        CustomName.pack_forget()
        if CheckName.get() == 1:
            CustomName.pack(pady=5)
        # folder_name_label.pack_forget()
        # folder_name_label.pack(pady=5)
        # folder.pack_forget()
        # folder.pack(pady=10)

def Disable(*args):
    if wyborcodeca.get() != 'mp3':
        mp3jakosc.configure(state='disabled')
    else:
        mp3jakosc.configure(state='normal')

def IfChecked(*args):
    if CheckName.get() == 1:
        CustomName.pack(padx=5, pady=5)
        CustomName.configure(state = 'normal')
    else:
        CustomName.pack_forget()
        CustomName.configure(state = 'disabled')

def search_yt(text):
    if text.find("www.youtube.com") == -1:
        try:
            result = YoutubeSearch(text, max_results=1).to_dict()
            return("http://www.youtube.com" + result[0].get("url_suffix"))
        except:
            return "EMPTY"
    return text

def startDownload(*args):
    if wybor.get() == 'Muzyka':
        try:
            codec = wyborcodeca.get()
        except:
            finishLabel.configure(text='Coś poszło nie tak z wyborem codeca', text_color = 'red')
        # codec = 'wav'
        # codec = 'flac'
        # print(browse_folder())
        try:
            quality = mp3jakosc.get()
        except:
            finishLabel.configure(text='Coś poszło nie tak z wyborem jakości mp3', text_color = 'red')

        try:
            ytLink = link.get()
            url = search_yt(ytLink)
            link.delete(0, 'end')
        except:
            finishLabel.configure(text='Coś jest nie tak z linkiem', text_color = 'red')
        
        ydl_opts['postprocessors'][0]['preferredcodec'] = codec
        ydl_opts['postprocessors'][0]['preferredquality'] = quality
        
        # if folder.get() == 1:
        #     ydl_opts['outtmpl'] = 'audio/%(title)s'
        # else:
        #     ydl_opts['outtmpl'] = '%(title)s'
        try:
            if folder_path_label.cget('text'):
                path = folder_path_label.cget('text')
                if CheckName.get() == 1:
                    text = CustomName.get()
                    output = f"/{text}.%(ext)s"
                    ydl_opts['outtmpl'] = path + output
                    CustomName.delete(0, 'end')
                    CheckName.deselect()
                else:
                    ydl_opts['outtmpl'] = path + '/%(title)s'
            else:
                if CheckName.get() == 1:
                    text = CustomName.get()
                    output = f"/{text}.%(ext)s"
                    ydl_opts['outtmpl'] = output
                    CustomName.delete(0, 'end')
                    CheckName.deselect()
                else:
                    ydl_opts['outtmpl'] = '%(title)s'
        except:
            finishLabel.configure(text='Coś jest nie tak z nazwą pliku lub ścieżką pliku', text_color = 'red')

        # w razie czego, bo coś czasami nie znika
        CustomName.pack_forget()
        try:
            if url == 'EMPTY':
                finishLabel.configure(text='Nie podano żadnego linku/słów kluczy', text_color = 'red')
            else:          
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    title = info_dict['title']
                    # filesize = info_dict['filesize']
                    # print('File Size: ' + str(filesize))
                    ydl.download([url])
                finishLabel.configure(text=f'Pobrano: {title}')
        except:
            finishLabel.configure(text='Coś poszło nie tak', text_color = 'red')
    else:
        try:
            ext = wyborextension.get()
        except:
            finishLabel.configure(text='Coś poszło nie tak z wyborem rozdzielczości', text_color = 'red')
        
        #jak sie ustawi rozszerzenie na mov to zmieni webm (jak da sie sam webmp to zmienia na mkv)
        if ext == 'webm':
            ext = 'mov'
        
        #mkv jest wykrywane jako webm, a webm jest wykrywany jako mkv
        if ext == 'mkv':
            ext = 'webm'

        try:
            rozd = mp4rozdzielczosc.get()
        except:
            finishLabel.configure(text='Coś poszło nie tak z wyborem rozdzielczości', text_color = 'red')
        try:
            ytLink = link.get()
            url = search_yt(ytLink)
            link.delete(0, 'end')
        except:
            finishLabel.configure(text='Coś jest nie tak z linkiem', text_color = 'red')

        ydl_opts2['format'] = f'bestvideo[ext={ext}][height<={rozd}]+bestaudio[ext=m4a]/bestvideo[height<={rozd}]+bestaudio'

        try:
            if folder_path_label.cget('text'):
                path = folder_path_label.cget('text')

                if CheckName.get() == 1:
                    text = CustomName.get()
                    output = f"/{text}.%(ext)s"
                    ydl_opts2['outtmpl'] = path + output
                    CustomName.delete(0, 'end')
                    CheckName.deselect()
                else:
                    ydl_opts2['outtmpl'] = path + '/%(title)s'
            else:
                if CheckName.get() == 1:
                    text = CustomName.get()
                    output = f"/{text}.%(ext)s"
                    ydl_opts2['outtmpl'] = output
                    CustomName.delete(0, 'end')
                    CheckName.deselect()
                else:
                    ydl_opts2['outtmpl'] = '%(title)s'
        except:
            finishLabel.configure(text='Coś jest nie tak z nazwą pliku lub ścieżką pliku', text_color = 'red')

        # w razie czego, bo coś czasami nie znika
        CustomName.pack_forget()
        try:
            if url == 'EMPTY':
                finishLabel.configure(text='Nie podano żadnego linku/słów kluczy', text_color = 'red')
            else:          
                with yt_dlp.YoutubeDL(ydl_opts2) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    title = info_dict['title']
                    # filesize = info_dict['filesize']
                    # print('File Size: ' + str(filesize))
                    ydl.download([url])
                finishLabel.configure(text=f'Pobrano: {title}')
        except:
            finishLabel.configure(text='Dana rozdzielczość jest nieobsługiwana przez podane wideo', text_color = 'red')

def clear_entry(event):
    if event.state & 0x4 and event.keysym == 'BackSpace':
        link.delete(0, 'end')

def clear_entry2(event):
    if event.state & 0x4 and event.keysym == 'BackSpace':
        CustomName.delete(0, 'end')

def startDownloadthreading():
    download_thread = threading.Thread(target=startDownload)
    download_thread.start()

def do_paste(event):
    try:
        clipboard_content = app.clipboard_get()
        event.widget.delete(0, tkinter.END)
        event.widget.insert(0, clipboard_content)
    except tkinter.TclError as e:
        print("Clipboard operation failed:", e)

def do_select_all(event):
    event.widget.focus()
    if isinstance(event.widget, tkinter.Entry):
        event.widget.select_range(0, tkinter.END)
    elif isinstance(event.widget, tkinter.Text):
        event.widget.tag_add("sel", "1.0", tkinter.END)

def do_popup(event):
    try:
        m.delete(0, tkinter.END)
        m.add_command(label="Copy", command=lambda: event.widget.event_generate('<<Copy>>'))
        m.add_command(label="Paste", command=lambda: do_paste(event))
        m.add_command(label="Cut", command=lambda: event.widget.event_generate('<<Cut>>'))
        m.add_command(label="Select All", command=lambda: do_select_all(event))
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

font=customtkinter.CTkFont(family='Open Sans', size=14, weight='bold')
font2=customtkinter.CTkFont(family='Open Sans', size=16, weight='bold')
font3=customtkinter.CTkFont(family='Open Sans', size=14)

title = customtkinter.CTkLabel(app, text='Podaj link lub słowa klucze', font=font2)
title.pack(padx=10, pady=10)

theme = customtkinter.CTkButton(app, text = 'Motyw', width=60, height=30, font=font, text_color="gainsboro", fg_color='gray38', command=lambda m="ciemny": JakiTheme(m))
theme.place(anchor='ne', relx = 0.98, rely = 0.03)

info = customtkinter.CTkButton(app, text = 'Info', width=60, height=30, font=font, command=lambda m="info": ShowCommands(m))
info.place(anchor='nw', relx = 0.02, rely = 0.03)

help = customtkinter.CTkLabel(app, text='MUZYKA\nOpcja ta pozwala pobrać muzykę w formacie mp3.\nMożna wybrać bitrate (w kbps), im wyższy bitrate tym lepsza jakość,\nale i plik będzie ważyć więcej. ' + 
                              'Jeżeli nie wiesz,\nczym jest bitrate, zalecam ustawić bitate na 192\n(czyli tyle, ile jest ustawione początkowo).\n\nWIDEO\nOpcja ta pozwala pobrać wideo w formacie mp4.\n'+
                              'Można wybrać jakość, im wyższa jakość\ntym wideo będzie ładniejsze i bardziej szczegółowe.\nWyższa jakość oznacza, że plik będzie ważył więcej.\nJeżeli nie wiesz jaką jakość ustawić, '+
                              'zalecam 720 lub 1080.\nJeżeli dane wideo nie obsługuje wybranej przez ciebie jakości,\nprogram pobierze wideo w najwyższej możliwej jakości.\n\nPOZOSTAŁE INFORMACJE:\n- Muzyka oraz wideo można wyszukać '+
                              'za pomocą linku\nlub słowa kluczy czy odpowiedniej frazy, dzięki której\n znajdziesz muzykę/film na youtube. Działają również playlisty.\n- Jeżeli nie wybierzesz miejsca zapisu pliku,\nprogram zapisze ' + 
                              'plik w miejscu, gdzie\nznajduje się program na twoim komputerze', font=font2)

url = customtkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url, font=font3)
# link.bind("<Return>", command=startDownload)
link.bind("<Return>", lambda event: threading.Thread(target=startDownload).start())
link.bind('<Key>', clear_entry)
link.pack()

finishLabel = customtkinter.CTkLabel(app, text='', font=font3)
finishLabel.pack(pady=5)

wybor = customtkinter.CTkSegmentedButton(app, font=font, values=["Muzyka", "Wideo"], command=WidocznoscElementow)
wybor.pack(pady=5)
wybor.set("Muzyka")

jakoscLabel = customtkinter.CTkLabel(app, text='Bitrate (w kbps)', font=font)
jakoscLabel.pack()

wyborcodeca = customtkinter.CTkOptionMenu(option_frame, width=80, font=font3, values=codecs, command=Disable)
wyborcodeca.pack(side='left', pady=5, padx=5)
wyborcodeca.set('mp3')

mp3jakosc = customtkinter.CTkOptionMenu(option_frame, width=80, font=font3, values=jakosc)
# mp3jakosc = customtkinter.CTkComboBox(app, values=jakosc)
mp3jakosc.pack(pady=5, padx=5)
mp3jakosc.set('192')

wyborextension = customtkinter.CTkOptionMenu(option_frame, width=80, font=font3, values=extensions)
# wyborcodeca.pack(side='left', pady=5, padx=5)
wyborextension.set('mp4')

mp4rozdzielczosc = customtkinter.CTkOptionMenu(option_frame, width=80, font=font3, values=rozdzielczosc)
# mp3jakosc = customtkinter.CTkComboBox(app, values=jakosc)
# mp4rozdzielczosc.pack(pady=5)
mp4rozdzielczosc.set('720')

option_frame.pack()
# folder = customtkinter.CTkCheckBox(app, text = 'W folderze')
# folder.pack(pady=10)

# Create the button and the label
browse_button = customtkinter.CTkButton(app, text="Wybierz miejsce\nzapisu", width=90, height=50, font=font, command=browse_folder)
folder_path_label = customtkinter.CTkLabel(app, text="")
# folder_name_label = customtkinter.CTkLabel(app, text="")
# Add the button and the label to the window
browse_button.pack(pady=5)

# font2=customtkinter.CTkFont(family='Open Sans', size=14, weight='bold')
download = customtkinter.CTkButton(app, text='Pobierz', width=90, height=40, font=font, command=lambda: startDownloadthreading())
# download.bind("<Return>", startDownload)
download.pack(padx=10, pady=5)
# folder_path_label.pack()
# folder_name_label.pack(pady=5)
CheckName = customtkinter.CTkCheckBox(app, text='Własna nazwa', font=font, command=IfChecked)
CheckName.pack(pady=5)

CustomName = customtkinter.CTkEntry(app, width=250, height=30, font=font3, state = 'disabled')
CustomName.bind("<Return>", lambda event: threading.Thread(target=startDownload).start())
CustomName.bind('<Key>', clear_entry2)

m = tkinter.Menu(app, tearoff = 0) 
link.bind("<Button-3>", do_popup)

app.drop_target_register(DND_FILES)
app.dnd_bind("<<Drop>>", get_path)
#wersja z pytube   
#------------ 
# def startDownload():
#     try:

#         url = link.get()
#         ytLink = search_yt(url)
#         if ytLink == "EMPTY":
#             print("Nie mogę otworzyć tego filmiku, spróbuj ponownie")
#         elif ytLink.startswith('https://www.youtube.com/playlist'):
#             playlist = Playlist(ytLink)
#             for video in playlist.videos:
#                 video = video.streams.filter(only_audio=True).first()
#                 out_file = video.download()
#                 base, ext = os.path.splitext(out_file)
#                 new_file = base + '.mp3'
#                 os.rename(out_file, new_file)
#         else:
#             ytObject = YouTube(ytLink)
#             # video = ytObject.streams.filter(only_audio=True).first()
#             video = ytObject.streams.get_audio_only()
#             # name = ytObject.streams[0].title
            
#             out_file = video.download()
#             base, ext = os.path.splitext(out_file)
#             new_file = base + '.mp3'
#             os.rename(out_file, new_file)

#         print('Pobrane!')
#     except:
#         print('Coś nie działa')        

# def onReturn(*args):
#     print('Pressed')

app.mainloop()