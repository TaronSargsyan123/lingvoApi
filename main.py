from tkinter import ttk
import requests
from config import *
from tkinter import *
import pytesseract
import cv2
import speech_recognition as sr
import os


pytesseract.pytesseract.tesseract_cmd = r"path to tesseract"
photoFile = "not path"




def photoButton():
    print(photoFile)
    if os.path.isfile(photoFile):
        try:
            img = cv2.imread(photoFile)
            wordCV = pytesseract.image_to_string(img, lang=cvLang).lower()
            print(wordCV.strip())
            txt.insert(0, wordCV.strip())
        except:
            print("pytesseract error")
    else:
        print("please enter path")




def fileButton():
    def tempButton():
        global photoFile
        photoFile = os.path.normpath(txt2.get())
        print(photoFile)
        txt2.destroy()
        tempBtn.destroy()


    txt2 = Entry(window, bg="#2D2F34", fg="#4D7992")
    txt2.place(x=(windowWidth/100)*5, y=(windowHeight/100)*80, width=(windowWidth/100)*90, height=(windowHeight/100)*5)

    tempBtn = Button(window, text="OK", command=tempButton, bg="#27292D", fg="#4D7992", activebackground='#27292D', highlightthickness=0)
    tempBtn.place(x=(windowWidth/100)*5, y=(windowHeight/100)*87, width=(windowWidth/100)*90, height=(windowHeight/100)*5)




headerAuth = {'Authorization': 'Basic ' + api_key}
auth = requests.post(URL_AUTH, headers=headerAuth)

srcLang = ENG
dstLang = RU
audioSrcLang = audioLanguageENG
audioDstLang = audioLanguageENG


def clicked():
    if auth.status_code == 200:
        global audioSrcLang
        global cvLang
        global audioDstLang
        if comboSRC.get() == "English":
            srcLang = ENG
            audioSrcLang = audioLanguageENG
            cvLang = cvLanguageENG
        elif comboSRC.get() =="Russian":
            srcLang = RU
            audioSrcLang = audioLanguageRU
            cvLang = cvLanguageRU
        elif comboSRC.get() =="Italian":
            srcLang = IT
        elif comboSRC.get() =="French":
            srcLang = FR

        if comboDST.get() == "English":
            dstLang = ENG
            audioDstLang = audioLanguageENG
        elif comboDST.get() =="Russian":
            dstLang = RU
            audioDstLang = audioLanguageRU
        elif comboDST.get() =="Italian":
            dstLang = IT
        elif comboDST.get() =="French":
            dstLang = FR




        token = auth.text
        translatWord = txt.get()

        headers_translate = {'Authorization': 'Bearer ' + token}
        params = {'text': translatWord, 'srcLang': srcLang, 'dstLang': dstLang}
        r = requests.get(URL_TRANSLATE, headers=headers_translate, params=params)
        res = r.json()

        try:
            lbl.configure(text=res['Translation']['Translation'])
        except:
            lbl.configure(text=RuError1)
    else:
        print("ERROR NO CONNECTION")


def audioButton():
    r = sr.Recognizer()

    with sr.Microphone(device_index=0) as source:

        print("Listen")

        audio = r.listen(source)

    audioWord = r.recognize_google(audio, language=audioSrcLang)
    print(audioWord.lower())
    txt.delete(0, 'end')
    txt.insert(0,audioWord)






window = Tk()
window.title("LingvoAPI translator")
window.resizable(False, False)
windowWidth = 300
windowHeight = 500
window.geometry(str(windowWidth)+"x"+str(windowHeight))
window.configure(bg="#27292D")






txt = Entry(window, bg="#2D2F34", fg="#4D7992")
txt.place(x=(windowWidth/100)*4, y=(windowHeight/100)*15, width=(windowWidth/100)*44, height=(windowHeight/100)*40)

lbl = Label(window,bg="#38393D", fg="#4D7992",anchor =NW,wraplength=110)
lbl.place(x=(windowWidth/100)*52, y=(windowHeight/100)*15, width=(windowWidth/100)*44, height=(windowHeight/100)*40)

translateBtn = Button(window, text="Translate", command=clicked, bg="#27292D", fg="#4D7992", activebackground='#27292D', highlightthickness=0)
translateBtn.place(x=(windowWidth/100)*28, y=(windowHeight/100)*60, width=(windowWidth/100)*48, height=(windowHeight/100)*5)

photoBtn = Button(window, text="Photo", command=photoButton, bg="#27292D", fg="#4D7992", activebackground='#27292D', highlightthickness=0)
photoBtn.place(x=(windowWidth/100)*80, y=(windowHeight/100)*60, width=(windowWidth/100)*15, height=(windowHeight/100)*5)

fileBtn = Button(window, text="File", command=fileButton, bg="#27292D", fg="#4D7992", activebackground='#27292D', highlightthickness=0)
fileBtn.place(x=(windowWidth/100)*80, y=(windowHeight/100)*67, width=(windowWidth/100)*15, height=(windowHeight/100)*5)

audioBtn = Button(window, text="Audio", command=audioButton, bg="#27292D", fg="#4D7992", activebackground='#27292D', highlightthickness=0)
audioBtn.place(x=(windowWidth/100)*5, y=(windowHeight/100)*60, width=(windowWidth/100)*15, height=(windowHeight/100)*5)

style= ttk.Style()
style.theme_use('clam')
style.configure("TCombobox",foreground="#4D7992",background="#27292D",fieldbackground="#27292D",darkcolor="#27292D",lightcolor="#27292D",selectbackground="#27292D",selectforeground="#27292D",bordercolor="#27292D",insertcolor="#27292D",insertwidth="#27292D",arrowsize="#27292D",arrowcolor="#4D7992",)


comboSRC = ttk.Combobox(window, style="TCombobox")
comboSRC['values'] = ("English", "Russian", "Italian", "French")
comboSRC.current(0)
comboSRC.place(x=(windowWidth/100)*4, y=(windowHeight/100)*5, width=(windowWidth/100)*44, height=(windowHeight/100)*5)

comboDST = ttk.Combobox(window)
comboDST['values'] = ("English", "Russian", "Italian", "French")
comboDST.current(1)
comboDST.place(x=(windowWidth/100)*52, y=(windowHeight/100)*5, width=(windowWidth/100)*44, height=(windowHeight/100)*5)



lbl1 = Label(window, text="translator by Taron Sargsyan", bg="#27292D", fg="#4D7992")
lbl1.place(x=0, y=(windowHeight/100)*95)




window.mainloop()

